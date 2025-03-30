from typing import Optional, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    name: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    unset: bool = Field(default=False)

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
