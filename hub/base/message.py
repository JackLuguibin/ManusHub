from typing import Optional, List

from pydantic import BaseModel, Field

from hub.base.role import Role


class Message(BaseModel):
    role: ROLE_TYPE = Field(...)  # type: ignore
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)

    def __add__(self, other) -> List["Message"]:
        if isinstance(other, Message):
            return [self, other]
        elif (
                isinstance(other, list) and
                all(isinstance(m, Message) for m in other)
        ):
            return [self] + other
        else:
            raise TypeError(
                "Unsupported operand type(s) for +: "
                f"'{type(self).__name__}' and '{type(other).__name__}'"
            )

    def __radd__(self, other)->List["Message"]:
        if isinstance(other, list):
            return other + [self]
        else:
            raise TypeError(
                "Unsupported operand type(s) for +: "
                f"'{type(other).__name__}' and '{type(self).__name__}'"
            )

    @classmethod
    def user_message(cls, content: str) -> "Message":
        return cls(role=Role.USER, content=content)

    @classmethod
    def system_message(cls, content: str) -> "Message":
        return cls(role=Role.SYSTEM, content=content)
