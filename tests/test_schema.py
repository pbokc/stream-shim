import pytest
from schemas import ChatCompletionRequest, ChatMessage


def test_request_schema_valid():
    req = ChatCompletionRequest(
        model="local", messages=[ChatMessage(role="user", content="hi")]
    )
    assert req.model == "local"
    assert req.messages[0].content == "hi"


def test_request_schema_rejects_bad_role():
    with pytest.raises(Exception):
        ChatMessage(role="bad", content="x")  # Literal check
