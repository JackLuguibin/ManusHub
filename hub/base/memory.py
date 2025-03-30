from typing import List, NoReturn

from pydantic import BaseModel, Field

from hub.base.message import Message


class Memory(BaseModel):
    messages: List["Message"] = Field(default_factory=list)
    max_size: int = Field(default=1000)

    def add_message(self, message: Message) -> None:
        if len(self.messages) >= self.max_size:
            self.messages.pop(0)
        self.messages.append(message)

    def add_messages(self, messages: List["Message"]) -> None:
        self.messages.extend(messages)
        self.messages = self.messages[-self.max_size:]

    def get_recent_messages(self, n: int) -> List["Message"]:
        return self.messages[-n:]

    def clear(self) -> None:
        self.messages.clear()

    def store(self) -> None:
        pass
