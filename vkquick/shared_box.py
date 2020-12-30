import dataclasses
import typing as ty

from vkquick.api import API
from vkquick.events_generators.longpoll import LongPollBase
from vkquick.utils import AttrDict

if ty.TYPE_CHECKING:
    from vkquick.bot import Bot


@dataclasses.dataclass
class SharedBox:

    api: ty.Optional[API] = None
    events_generator: ty.Optional[LongPollBase] = None
    bot: ty.Optional["Bot"] = None
    extra: AttrDict = dataclasses.field(default_factory=AttrDict)
