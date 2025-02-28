import logging
from typing import TYPE_CHECKING, Optional

from maufbapi.types import mqtt as mqtt_t
from maufbapi.types.graphql import ParticipantNode, Thread
from maufbapi.types.graphql.responses import FriendshipStatus
from slidge import LegacyContact, LegacyRoster
from slixmpp.exceptions import XMPPError

from .util import ChatterMixin, is_group_thread

if TYPE_CHECKING:
    from .session import Session


class Contact(ChatterMixin, LegacyContact[int]):
    CORRECTION = False
    REACTIONS_SINGLE_EMOJI = True
    session: "Session"

    def __init__(
        self,
        session: "Session",
        legacy_id: int,
        jid_username: str,
        participant: Optional[ParticipantNode] = None,
    ):
        super().__init__(session, legacy_id, jid_username)
        if participant is not None:
            self.populate_from_participant(participant)

    @property
    def fb_id(self):
        return self.legacy_id

    def populate_from_participant(
        self, participant: ParticipantNode, update_avatar=True
    ):
        if self.legacy_id != int(participant.messaging_actor.id):
            raise XMPPError(
                "bad-request",
                (
                    f"Legacy ID {self.legacy_id} does not match participant"
                    f" {participant.messaging_actor.id}"
                ),
            )
        self.is_friend = (
            participant.messaging_actor.friendship_status
            == FriendshipStatus.ARE_FRIENDS
        )
        self.name = participant.messaging_actor.name
        if self.avatar is None or update_avatar:
            pic = participant.messaging_actor.profile_pic_large
            self.avatar = pic.uri

    async def get_thread(self, **kwargs):
        threads = await self.session.api.fetch_thread_info(self.legacy_id, **kwargs)
        if len(threads) != 1:
            self.log.debug("Could not determine my profile! %s", threads)
            raise XMPPError(
                "internal-server-error",
                f"The messenger API returned {len(threads)} threads for this user.",
            )
        return threads[0]

    async def update_info(self, refresh=False):
        if self.name and not refresh:
            return
        t = await self.get_thread(msg_count=0)

        participant = self.session.contacts.get_friend_participant(
            t.all_participants.nodes
        )
        self.populate_from_participant(participant)


class Roster(LegacyRoster[int, Contact]):
    session: "Session"

    async def by_thread_key(self, t: mqtt_t.ThreadKey):
        if is_group_thread(t):
            raise ValueError("Thread seems to be a group thread")
        c = await self.by_legacy_id(t.other_user_id)
        await c.add_to_roster()
        return c

    async def by_thread(self, t: Thread):
        if t.is_group_thread:
            raise XMPPError(
                "bad-request", f"Legacy ID {t.id} is a group chat, not a contact"
            )

        participant = self.get_friend_participant(t.all_participants.nodes)
        fb_id = int(participant.messaging_actor.id)
        contact = await self.by_legacy_id(fb_id, participant)
        return contact

    def get_friend_participant(self, nodes: list[ParticipantNode]) -> ParticipantNode:
        if len(nodes) != 2:
            raise XMPPError(
                "internal-server-error",
                (
                    "This facebook thread has more than two participants. This is a"
                    " slidge bug."
                ),
            )

        for participant in nodes:
            if int(participant.id) != self.session.my_id:
                return participant
        else:
            raise XMPPError(
                "internal-server-error", "Couldn't find friend in thread participants"
            )


log = logging.getLogger(__name__)
