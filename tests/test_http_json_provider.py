import respx, httpx, pytest
from providers.http_json import HttpJson


@pytest.mark.anyio
async def test_http_json_success(monkeypatch):
    # Override the UPSTREAM_URL in the http_json module
    import providers.http_json

    monkeypatch.setattr(
        providers.http_json, "UPSTREAM_URL", "http://127.0.0.1:5001/generate"
    )

    prov = HttpJson()
    with respx.mock:
        respx.post("http://127.0.0.1:5001/generate").mock(
            return_value=httpx.Response(200, json={"text": "ok"})
        )
        text = await prov.generate("hi")
        assert text == "ok"


@pytest.mark.anyio
async def test_http_json_missing_text(monkeypatch):
    # Override the UPSTREAM_URL in the http_json module
    import providers.http_json

    monkeypatch.setattr(
        providers.http_json, "UPSTREAM_URL", "http://127.0.0.1:5001/generate"
    )

    prov = HttpJson()
    with respx.mock:
        respx.post("http://127.0.0.1:5001/generate").mock(
            return_value=httpx.Response(200, json={"nope": "x"})
        )
        with pytest.raises(Exception):
            await prov.generate("hi")


@pytest.mark.anyio
async def test_http_json_502():
    prov = HttpJson()
    with respx.mock:
        respx.post("http://127.0.0.1:5001/generate").mock(
            return_value=httpx.Response(500, json={"error": "boom"})
        )
        with pytest.raises(Exception):
            await prov.generate("hi")
