from pydantic import RootModel, HttpUrl, ConfigDict
from .base import ExtendBaseModel
from .extend import ArrowPydanticV2


class Project(ExtendBaseModel):
    model_config = ConfigDict(extra='ignore')

    id: int
    description: str | None
    name: str
    name_with_namespace: str
    created_at: ArrowPydanticV2
    last_activity_at: ArrowPydanticV2
    web_url: HttpUrl


class ProjectList(RootModel[list[Project]]):
    pass
