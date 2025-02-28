import maufbapi.http.api
from maufbapi.types.graphql import OwnInfo
from slidge.util.util import get_version  # noqa: F401

from . import config, contact, gateway, group, session

# workaround until https://github.com/mautrix/facebook/pull/318 is merged and
# released
maufbapi.http.api.OwnInfo = OwnInfo

__all__ = "config", "contact", "gateway", "group", "session"

__version__ = "v0.2.0"
