from app import join_messages
from schemas import ChatMessage


def test_join_messages():
    msgs = [
        ChatMessage(role="system", content="x"),
        ChatMessage(role="user", content="y"),
    ]
    out = join_messages(msgs)
    assert "system: x" in out and "user: y" in out
