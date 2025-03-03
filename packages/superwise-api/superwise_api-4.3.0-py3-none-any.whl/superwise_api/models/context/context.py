from pydantic import BaseModel

from superwise_api.models.tool.tool import ContextConfig


class ContextDef(BaseModel):
    name: str
    config: ContextConfig
