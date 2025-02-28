from datetime import datetime
from typing import TYPE_CHECKING, Optional

from maufbapi.types.graphql import Thread
from slidge import LegacyBookmarks, LegacyMUC, LegacyParticipant, MucType
from slidge.util.types import HoleBound
from slixmpp.exceptions import XMPPError

from .util import ChatterMixin

if TYPE_CHECKING:
    from .session import Session


class Bookmarks(LegacyBookmarks[int, "MUC"]):
    session: "Session"

    def __init__(self, session):
        super().__init__(session)
        self.threads = dict[int, Thread]()

    async def by_thread(self, thread: Thread):
        fb_id = int(thread.thread_key.thread_fbid)
        self.threads[fb_id] = thread
        return await self.by_legacy_id(fb_id)

    async def legacy_id_to_jid_local_part(self, i: int):
        return str(i)

    async def jid_local_part_to_legacy_id(self, local_part: str):
        try:
            return int(local_part)
        except ValueError:
            raise XMPPError(
                "item-not-found", f"Not a valid messenger chat id: {local_part}"
            )

    async def fill(self):
        pass


class MUC(LegacyMUC[int, str, "Participant", int]):
    session: "Session"

    type = MucType.GROUP
    REACTIONS_SINGLE_EMOJI = True
    _ALL_INFO_FILLED_ON_STARTUP = True

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.thread = None

    async def get_thread(self):
        thread = self.thread
        if not thread:
            thread = self.session.bookmarks.threads.pop(self.legacy_id, None)

        if not thread:
            try:
                threads = await self.session.api.fetch_thread_info(self.legacy_id)
            except Exception as e:
                raise XMPPError(
                    "internal-server-error", f"This group chat cannot be fetched: {e}"
                )
            if not threads:
                raise XMPPError("item-not-found")
            if not isinstance(threads, list) or len(threads) != 1:
                self.log.warning("Weird fetch_thread_info response: %s", threads)
                raise XMPPError(
                    "internal-server-error", f"Bad response from maufbapi: {threads}"
                )

            thread = threads[0]
        self.thread = thread
        return thread

    async def update_info(self, thread: Optional[Thread] = None):
        if not thread:
            thread = await self.get_thread()
        if thread.name:
            self.name = thread.name
        else:
            self.name = ", ".join(
                [
                    n.messaging_actor.name.split(" ")[0]
                    for n in thread.all_participants.nodes
                    if int(n.id) != self.session.contacts.user_legacy_id
                ]
            )
        if thread.image:
            if self.avatar != thread.image.uri:
                await self.set_avatar(thread.image.uri)
        else:
            self.avatar = None
        self.n_participants = len(thread.all_participants.nodes)

    async def fill_participants(self):
        t = await self.get_thread()
        self.log.debug("%s participants", len(t.all_participants.nodes))
        for p in t.all_participants.nodes:
            self.log.debug("participant: %s", p)
            if int(p.messaging_actor.id) == self.session.contacts.user_legacy_id:
                continue
            contact = await self.session.contacts.by_legacy_id(
                int(p.messaging_actor.id), p
            )
            part = await self.get_participant_by_contact(contact)
            self.log.debug("participant: %s", part)
            yield part

    async def backfill(
        self, after: Optional[HoleBound] = None, before: Optional[HoleBound] = None
    ):
        t = await self.get_thread()
        for m in t.messages.nodes:
            if not m.id:
                continue
            timestamp = datetime.fromtimestamp(m.timestamp / 1_000)
            if after is not None and timestamp < after.timestamp:
                continue
            if before is not None and timestamp > before.timestamp:
                continue
            part = await self.get_participant_by_legacy_id(
                int(m.message_sender.messaging_actor.id)
            )
            await part.send_fb_message(m)


class Participant(ChatterMixin, LegacyParticipant):
    @property
    def fb_id(self):
        return self.muc.legacy_id
