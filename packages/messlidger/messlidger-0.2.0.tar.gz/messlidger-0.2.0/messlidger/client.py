from typing import TYPE_CHECKING, Optional

from maufbapi import AndroidMQTT as AndroidMQTTOriginal
from maufbapi.types import mqtt as mqtt_t
from slidge.util.types import MessageReference

from .util import FacebookMessage, is_group_thread

REQUEST_TIMEOUT = 60

if TYPE_CHECKING:
    from .session import Session


class AndroidMQTT(AndroidMQTTOriginal):
    def __init__(
        self,
        session: "Session",
        state,
        loop=None,
        log=None,
        connect_token_hash=None,
        proxy_handler=None,
    ):
        # overrides the default init to enable presences
        self.session = session
        super().__init__(state, loop, log, connect_token_hash, proxy_handler)

    def register_handlers(self):
        self.seq_id_update_callback = lambda i: setattr(  # type:ignore
            self, "seq_id", i
        )
        self.add_event_handler(mqtt_t.Message, self.on_fb_message)
        self.add_event_handler(mqtt_t.ExtendedMessage, self.on_fb_extended_message)
        self.add_event_handler(mqtt_t.ReadReceipt, self.on_fb_message_read)
        self.add_event_handler(mqtt_t.TypingNotification, self.on_fb_typing)
        self.add_event_handler(mqtt_t.OwnReadReceipt, self.on_fb_user_read)
        self.add_event_handler(mqtt_t.Reaction, self.on_fb_reaction)
        self.add_event_handler(mqtt_t.UnsendMessage, self.on_fb_unsend)

        self.add_event_handler(mqtt_t.AvatarChange, self.on_fb_event)
        self.add_event_handler(mqtt_t.AddMember, self.on_fb_event)
        self.add_event_handler(mqtt_t.RemoveMember, self.on_fb_event)

        self.add_event_handler(mqtt_t.NameChange, self.on_fb_event)
        self.add_event_handler(mqtt_t.ThreadChange, self.on_fb_event)
        self.add_event_handler(mqtt_t.MessageSyncError, self.on_fb_event)
        self.add_event_handler(mqtt_t.ForcedFetch, self.on_fb_event)

    async def __get_chatter(
        self, thread_key: mqtt_t.ThreadKey, fb_id: Optional[int] = None
    ):
        if is_group_thread(thread_key):
            self.log.debug("MUC")
            muc = await self.session.bookmarks.by_legacy_id(thread_key.thread_fbid)
            self.log.debug("MUC %s", muc)
            if fb_id:
                self.log.debug("fbid: %s", fb_id)
                chatter = await muc.get_participant_by_legacy_id(fb_id)
            else:
                self.log.debug("no fbid: %s", fb_id)
                chatter = await muc.get_user_participant()
            self.log.debug("chatter: %s", chatter)
        else:
            chatter = await self.session.contacts.by_thread_key(thread_key)
        return chatter

    async def on_fb_extended_message(self, evt: mqtt_t.ExtendedMessage):
        self.log.debug("Extended message")
        kwargs = {}
        msg = evt.message

        if reply_to_fb_msg := evt.reply_to_message:
            self.log.debug("Reply-to")
            author_fb_id = reply_to_fb_msg.metadata.sender
            if author_fb_id == self.session.my_id:
                author = "user"  # type: ignore
            else:
                author = await self.session.contacts.by_legacy_id(author_fb_id)  # type: ignore
            kwargs["reply_to"] = MessageReference(
                legacy_id=reply_to_fb_msg.metadata.id,
                body=reply_to_fb_msg.text,
                author=author,  # type: ignore
            )
        await self.on_fb_message(msg, **kwargs)

    async def on_fb_message(self, msg: mqtt_t.Message, **kwargs):
        meta = msg.metadata
        chatter = await self.__get_chatter(meta.thread, meta.sender)
        fb_msg = FacebookMessage(mid=meta.id, timestamp_ms=meta.timestamp)

        if meta.sender == self.session.my_id:
            try:
                fut = self.session.ack_futures.pop(meta.offline_threading_id)
            except KeyError:
                self.log.debug("Received carbon %s - %s", meta.id, msg.text)
                kwargs["carbon"] = True
                self.log.debug("Sent carbon")
                self.session.sent_messages[chatter.fb_id].add(fb_msg)
            else:
                self.log.debug("Received echo of %s", meta.offline_threading_id)
                fut.set_result(fb_msg)
                return
        else:
            self.session.received_messages[chatter.fb_id].add(fb_msg)

        await chatter.send_fb_message(msg, **kwargs)

    async def on_fb_message_read(self, receipt: mqtt_t.ReadReceipt):
        self.log.debug("Facebook read: %s", receipt)
        chatter = await self.__get_chatter(receipt.thread, receipt.user_id)
        try:
            mid = (
                self.session.sent_messages[chatter.fb_id].pop_up_to(receipt.read_to).mid
            )
        except KeyError:
            self.log.debug("Cannot find MID of %s", receipt.read_to)
        else:
            chatter.displayed(mid)

    async def on_fb_typing(self, notification: mqtt_t.TypingNotification):
        self.log.debug("Facebook typing: %s", notification)
        c = await self.session.contacts.by_legacy_id(notification.user_id)
        if notification.typing_status:
            c.composing()
        else:
            c.paused()

    async def on_fb_user_read(self, receipt: mqtt_t.OwnReadReceipt):
        self.log.debug("Facebook own read: %s", receipt)
        when = receipt.read_to
        for thread in receipt.threads:
            c = await self.__get_chatter(thread)
            try:
                mid = self.session.received_messages[c.fb_id].pop_up_to(when).mid
            except KeyError:
                self.log.debug("Cannot find mid of %s", when)
                continue
            c.displayed(mid, carbon=True)

    async def on_fb_reaction(self, reaction: mqtt_t.Reaction):
        self.log.debug("Reaction: %s", reaction)
        chatter = await self.__get_chatter(reaction.thread, reaction.reaction_sender_id)
        mid = reaction.message_id
        if reaction.reaction_sender_id == self.session.my_id:
            try:
                f = self.session.reaction_futures.pop(mid)
            except KeyError:
                chatter.react(mid, reaction.reaction or "", carbon=True)
            else:
                f.set_result(None)
        else:
            chatter.react(reaction.message_id, reaction.reaction or "")

    async def on_fb_unsend(self, unsend: mqtt_t.UnsendMessage):
        self.log.debug("Unsend: %s", unsend)
        chatter = await self.__get_chatter(unsend.thread, unsend.user_id)
        mid = unsend.message_id
        if unsend.user_id == self.session.my_id:
            try:
                f = self.session.unsend_futures.pop(mid)
            except KeyError:
                chatter.retract(mid, carbon=True)
            else:
                f.set_result(None)
        else:
            chatter.retract(unsend.message_id)

    async def on_fb_event(self, evt):
        self.log.debug("Facebook event: %s", evt)
