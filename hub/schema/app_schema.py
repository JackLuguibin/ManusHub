from typing import Dict

from pydantic import BaseModel

from hub.schema.llm_schema import LLMSettings


class AppSchema(BaseModel):
    llm:Dict[str, LLMSettings]

    class Config:
        arbitrary_types_allowed = True