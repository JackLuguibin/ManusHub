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
    def make_user_message(cls, content: str) -> "Message":
        return cls(role=Role.USER, content=content)

    @classmethod
    def make_system_message(cls, content: str) -> "Message":
        return cls(role=Role.SYSTEM, content=content)

    @classmethod
    def make_assistant_message(cls, content: str) -> "Message":
        return cls(role=Role.ASSISTANT, content=content)
    @classmethod
    def make_tool_message(cls, content: str) -> "Message":
        return cls(role=Role.TOOL, content=content)

MESSAGE_MAKERS = {
    Role.USER: Message.make_user_message,
    Role.SYSTEM: Message.make_system_message,
    Role.ASSISTANT: Message.make_assistant_message,
    Role.TOOL: Message.make_tool_message,
}