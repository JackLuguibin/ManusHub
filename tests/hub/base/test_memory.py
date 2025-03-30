import pytest

from hub.base.memory import Memory
from hub.base.message import Message


def test_add_message():
    memory = Memory()
    message = Message(name="test_name", content="test_content")
    memory.add_message(message)
    assert len(memory.messages) == 1
    assert memory.messages[0] == message


def test_add_messages():
    memory = Memory()
    messages = [Message(name=f"name_{i}", content=f"content_{i}") for i in range(5)]
    memory.add_messages(messages)
    assert len(memory.messages) == 5
    assert memory.messages == messages


def test_get_recent_messages():
    memory = Memory()
    messages = [Message(name=f"name_{i}", content=f"content_{i}") for i in range(10)]
    memory.add_messages(messages)
    recent_messages = memory.get_recent_messages(3)
    assert len(recent_messages) == 3
    assert recent_messages == messages[-3:]


def test_clear():
    memory = Memory()
    messages = [Message(name=f"name_{i}", content=f"content_{i}") for i in range(5)]
    memory.add_messages(messages)
    memory.clear()
    assert len(memory.messages) == 0


def test_store():
    memory = Memory()
    memory.store()


if __name__ == "__main__":
    pytest.main(["-v", __file__])
