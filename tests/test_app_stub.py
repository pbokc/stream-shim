import pytest, anyio
from httpx import AsyncClient, ASGITransport
from app import app as fastapi_app


@pytest.mark.anyio
async def test_healthz():
    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        r = await ac.get("/healthz")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"


@pytest.mark.anyio
async def test_chat_stub_shape(monkeypatch):
    # Force provider.generate to return fixed string
    class Dummy:
        async def generate(self, prompt: str) -> str:
            return "hello world"

    # Patch get_provider in both the factory module and where it's imported in app
    import providers.factory

    monkeypatch.setattr(providers.factory, "get_provider", lambda: Dummy())

    # Also patch in the app module since it imports the function directly
    import app

    monkeypatch.setattr(app, "get_provider", lambda: Dummy())

    async with AsyncClient(
        transport=ASGITransport(app=fastapi_app), base_url="http://test"
    ) as ac:
        r = await ac.post(
            "/v1/chat/completions",
            json={"model": "local", "messages": [{"role": "user", "content": "test"}]},
        )
        j = r.json()
        assert r.status_code == 200
        assert j["choices"][0]["message"]["content"] == "hello world"
        assert j["model"] == "local"
