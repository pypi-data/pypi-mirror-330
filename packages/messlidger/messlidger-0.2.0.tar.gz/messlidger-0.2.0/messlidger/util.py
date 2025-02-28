import json
import shelve
from collections import OrderedDict
from dataclasses import dataclass
from typing import TYPE_CHECKING

from maufbapi import AndroidState
from maufbapi.types import mqtt as mqtt_t
from slidge import global_config
from slidge.core.mixins.attachment import AttachmentMixin
from slidge.util.types import LegacyAttachment

if TYPE_CHECKING:
    from .session import Session


def get_shelf_path(user_bare_jid):
    return str(global_config.HOME_DIR / user_bare_jid)


def save_state(user_bare_jid: str, state: AndroidState):
    shelf_path = get_shelf_path(user_bare_jid)
    with shelve.open(shelf_path) as shelf:
        shelf["state"] = state


@dataclass
class FacebookMessage:
    mid: str
    timestamp_ms: int


class Messages:
    def __init__(self):
        self.by_mid: OrderedDict[str, FacebookMessage] = OrderedDict()
        self.by_timestamp_ms: OrderedDict[int, FacebookMessage] = OrderedDict()

    def __len__(self):
        return len(self.by_mid)

    def add(self, m: FacebookMessage):
        self.by_mid[m.mid] = m
        self.by_timestamp_ms[m.timestamp_ms] = m

    def pop_up_to(self, approx_t: int) -> FacebookMessage:
        i = 0
        for i, t in enumerate(self.by_timestamp_ms.keys()):
            if t > approx_t:
                i -= 1
                break
        for j, t in enumerate(list(self.by_timestamp_ms.keys())):
            msg = self.by_timestamp_ms.pop(t)
            self.by_mid.pop(msg.mid)
            if j == i:
                return msg
        else:
            raise KeyError(approx_t)


def is_group_thread(t: mqtt_t.ThreadKey):
    return t.other_user_id is None and t.thread_fbid is not None


class ChatterMixin(AttachmentMixin):
    session: "Session"

    async def send_fb_message(self, msg: mqtt_t.Message, **kwargs):
        kwargs["legacy_msg_id"] = msg.metadata.id

        sticker = msg.sticker
        if sticker is not None:
            return await self.send_fb_sticker(sticker, **kwargs)

        text = msg.text or ""
        atts = []
        for a in msg.attachments:
            url = await self.get_attachment_url(a, msg.metadata.thread, msg.metadata.id)
            if url:
                atts.append(
                    LegacyAttachment(
                        name=a.file_name,
                        content_type=a.mime_type,
                        url=url,
                        legacy_file_id=a.media_id_str,
                    )
                )
            if not a.extensible_media:
                continue
            try:
                subtext, urls = self.get_extensible_media(a.extensible_media)
            except ValueError:
                self.send_text(f"/me sent something slidge does not understand: {a}")
                continue
            text += subtext
            atts.extend(
                LegacyAttachment(url=url, content_type="image/jpeg") for url in urls
            )

        await self.send_files(attachments=atts, body=text or None, **kwargs)

    def get_extensible_media(self, media: str) -> tuple[str, list[str]]:
        try:
            media_dict = json.loads(media)
        except Exception as e:
            self.session.log.warning("Could not decipher extensible media: %r", e)
            raise ValueError

        text = ""
        files = []
        for item in media_dict.values():
            story = item.get("story_attachment")
            if not story:
                continue
            url = story.get("url")
            if not url:
                continue

            text += f"\n{url}"

            if title := story.get("title"):
                text += f" - {title}"

            if desc := story.get("description"):
                if desc_text := desc.get("text"):
                    text += f" - {desc_text}"

            if attachment := story.get("media"):
                if image := attachment.get("image"):
                    if url := image.get("uri"):
                        files.append(url)

        if not text and not files:
            raise ValueError

        return text, files

    async def get_attachment_url(
        self, attachment: mqtt_t.Attachment, thread_key, msg_id
    ):
        try:
            if v := attachment.video_info:
                return v.download_url
            if a := attachment.audio_info:
                return a.url
            if i := attachment.image_info:
                return i.uri_map.get(0)
        except AttributeError:
            media_id = getattr(attachment, "media_id", None)
            if media_id:
                return await self.session.api.get_file_url(
                    thread_key.thread_fbid or thread_key.other_user_id,
                    msg_id,
                    media_id,
                )

    async def send_fb_sticker(self, sticker_id: int, legacy_msg_id: str, **kwargs):
        resp = await self.session.api.fetch_stickers([sticker_id])
        await self.send_file(
            file_url=resp.nodes[0].preview_image.uri,
            legacy_file_id=f"sticker-{sticker_id}",
            legacy_msg_id=legacy_msg_id,
            **kwargs,
        )
