from pydantic import Field
from kraph.links.upload import UploadLink
from rath import rath
import contextvars

from rath.links.auth import AuthTokenLink

from rath.links.compose import TypedComposedLink
from rath.links.dictinglink import DictingLink
from rath.links.shrink import ShrinkingLink
from rath.links.split import SplitLink

current_kraph_rath = contextvars.ContextVar("current_kraph_rath")


class KraphLinkComposition(TypedComposedLink):
    shrinking: ShrinkingLink = Field(default_factory=ShrinkingLink)
    dicting: DictingLink = Field(default_factory=DictingLink)
    upload: UploadLink
    auth: AuthTokenLink
    split: SplitLink


class KraphRath(rath.Rath):
    """Kraph Rath

    Args:
        rath (_type_): _description_
    """

    link: KraphLinkComposition = Field(default_factory=KraphLinkComposition)

    async def __aenter__(self):
        await super().__aenter__()
        current_kraph_rath.set(self)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        current_kraph_rath.set(None)
