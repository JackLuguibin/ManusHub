from hub.base.message import Message
import pytest


def test_message_add_message():
    msg1 = Message(name="msg1", content="content1")
    msg2 = Message(name="msg2", content="content2")
    result = msg1 + msg2
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == msg1
    assert result[1] == msg2


def test_message_add_list():
    msg1 = Message(name="msg1", content="content1")
    msg_list = [Message(name="msg2", content="content2")]
    result = msg1 + msg_list
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == msg1
    assert result[1] == msg_list[0]


def test_message_radd_list():
    msg1 = Message(name="msg1", content="content1")
    msg_list = [Message(name="msg2", content="content2")]
    result = msg_list + msg1
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0] == msg_list[0]
    assert result[1] == msg1


def test_message_add_unsupported_type():
    msg1 = Message(name="msg1", content="content1")
    with pytest.raises(TypeError):
        _ = msg1 + "not a message"


def test_message_radd_unsupported_type():
    msg1 = Message(name="msg1", content="content1")
    with pytest.raises(TypeError):
        _ = "not a list" + msg1


if __name__ == "__main__":
    pytest.main(["-v", __file__])
