import asyncio
import logging
import shelve
from collections import defaultdict
from typing import Union

import maufbapi.types
from maufbapi import AndroidAPI, AndroidState
from maufbapi.http import InvalidAccessToken
from maufbapi.types import mqtt as mqtt_t
from maufbapi.types.graphql import Participant
from mautrix.util.proxy import ProxyHandler
from slidge import BaseSession, FormField, SearchResult
from slixmpp.exceptions import XMPPError

from . import config
from .client import AndroidMQTT
from .contact import Contact, Roster
from .group import MUC, Bookmarks
from .util import FacebookMessage, Messages, get_shelf_path

Recipient = Union[Contact, MUC]


class Session(BaseSession[str, Recipient]):
    contacts: Roster
    bookmarks: Bookmarks

    mqtt: AndroidMQTT
    api: AndroidAPI
    me: maufbapi.types.graphql.OwnInfo
    my_id: int

    def __init__(self, user):
        super().__init__(user)

        # keys = "offline thread ID"
        self.ack_futures = dict[int, asyncio.Future[FacebookMessage]]()

        # keys = "facebook message id"
        self.reaction_futures = dict[str, asyncio.Future]()
        self.unsend_futures = dict[str, asyncio.Future]()

        # keys = "contact ID"
        self.sent_messages = defaultdict[int, Messages](Messages)
        self.received_messages = defaultdict[int, Messages](Messages)

    async def login(self):
        shelf: shelve.Shelf[AndroidState]
        with shelve.open(get_shelf_path(self.user_jid.bare)) as shelf:
            s = shelf["state"]
        x = ProxyHandler(None)
        self.api = AndroidAPI(state=s, proxy_handler=x)
        self.mqtt = AndroidMQTT(
            self, self.api.state, proxy_handler=self.api.proxy_handler
        )
        try:
            self.me = await self.api.get_self()
        except InvalidAccessToken:
            await self.xmpp.unregister_user(self.user)
            raise XMPPError(
                "not-authorized",
                "Your facebook access token has expired. "
                "Please re-register to the gateway.",
            )
        self.my_id = int(self.me.id)  # bug in maufbapi? tulir said: "ask meta"
        self.contacts.user_legacy_id = self.my_id
        await self.add_threads()
        self.mqtt.register_handlers()
        self.create_task(self.mqtt.listen(self.mqtt.seq_id))
        return f"Connected as '{self.me.name} <{self.me.email}>'"

    async def add_threads(self):
        thread_list = await self.api.fetch_thread_list(
            msg_count=0, thread_count=config.CHATS_TO_FETCH
        )
        self.mqtt.seq_id = int(thread_list.sync_sequence_id)  # type:ignore
        self.log.debug("SEQ ID: %s", self.mqtt.seq_id)
        self.log.debug("Thread list: %s", thread_list)
        self.log.debug("Thread list page info: %s", thread_list.page_info)
        contacts = []
        for t in thread_list.nodes:
            if t.is_group_thread:
                continue
            try:
                c = await self.contacts.by_thread(t)
            except XMPPError as e:
                self.log.warning(
                    "Something went wrong with this thread: %s", t, exc_info=e
                )
                continue
            contacts.append(c)
            await c.add_to_roster()
        for t in thread_list.nodes:
            if not t.is_group_thread:
                continue
            try:
                g = await self.bookmarks.by_thread(t)
            except XMPPError as e:
                self.log.warning(
                    "Something went wrong with this group thread: %s", t, exc_info=e
                )
                continue
            await g.add_to_bookmarks()
        for c in contacts:
            c.online()

    async def logout(self):
        pass

    async def on_text(
        self, chat: Recipient, text: str, *, reply_to_msg_id=None, **kwargs
    ) -> str:
        resp: mqtt_t.SendMessageResponse = await self.mqtt.send_message(
            target=chat.legacy_id,
            message=text,
            is_group=False,
            reply_to=reply_to_msg_id,
        )
        fut = self.ack_futures[
            resp.offline_threading_id
        ] = self.xmpp.loop.create_future()
        log.debug("Send message response: %s", resp)
        if not resp.success:
            raise XMPPError("internal-server-error", resp.error_message)
        fb_msg = await fut
        self.sent_messages[chat.legacy_id].add(fb_msg)
        return fb_msg.mid

    async def on_file(
        self, chat: Recipient, url: str, http_response, reply_to_msg_id=None, **_
    ):
        oti = self.mqtt.generate_offline_threading_id()
        fut = self.ack_futures[oti] = self.xmpp.loop.create_future()
        resp = await self.api.send_media(
            data=await http_response.read(),
            file_name=url.split("/")[-1],
            mimetype=http_response.content_type,
            offline_threading_id=oti,
            chat_id=chat.legacy_id,
            is_group=False,
            reply_to=reply_to_msg_id,
        )
        ack = await fut
        log.debug("Upload ack: %s", ack)
        return resp.media_id

    async def on_composing(self, c: Recipient, thread=None):
        await self.mqtt.set_typing(target=c.legacy_id)

    async def on_paused(self, c: Recipient, thread=None):
        await self.mqtt.set_typing(target=c.legacy_id, typing=False)

    async def on_displayed(self, c: Recipient, legacy_msg_id: str, thread=None):
        try:
            t = self.received_messages[c.legacy_id].by_mid[legacy_msg_id].timestamp_ms
        except KeyError:
            log.debug("Cannot find the timestamp of %s", legacy_msg_id)
        else:
            await self.mqtt.mark_read(target=c.legacy_id, read_to=t, is_group=False)

    async def on_react(
        self, c: Recipient, legacy_msg_id: str, emojis: list[str], thread=None
    ):
        # only one reaction per msg on facebook, but this is handled by slidge core
        if len(emojis) == 0:
            emoji = None
        else:
            emoji = emojis[-1]
        f = self.reaction_futures[legacy_msg_id] = self.xmpp.loop.create_future()
        await self.api.react(legacy_msg_id, emoji)
        await f

    async def on_retract(self, c: Recipient, legacy_msg_id: str, thread=None):
        f = self.unsend_futures[legacy_msg_id] = self.xmpp.loop.create_future()
        await self.api.unsend(legacy_msg_id)
        await f

    async def on_search(self, form_values: dict[str, str]) -> SearchResult:
        results = await self.api.search(form_values["query"], entity_types=["user"])
        log.debug("Search results: %s", results)
        items = []
        for search_result in results.search_results.edges:
            result = search_result.node
            if isinstance(result, Participant):
                try:
                    contact = await self.contacts.by_legacy_id(int(result.id))
                except XMPPError:
                    items.append(
                        {
                            "name": result.name + " (problem)",
                            "jid": "",
                        }
                    )
                    continue
                if contact.is_friend:
                    await contact.add_to_roster()
                items.append(
                    {
                        "name": (
                            result.name + " (friend)"
                            if contact.is_friend
                            else " (not friend)"
                        ),
                        "jid": contact.jid.bare,
                    }
                )

        return SearchResult(
            fields=[
                FormField(var="name", label="Name"),
                FormField(var="jid", label="JID", type="jid-single"),
            ],
            items=items,
        )


log = logging.getLogger(__name__)
