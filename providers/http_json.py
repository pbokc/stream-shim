import httpx
from fastapi import HTTPException
from .base import Provider
from config import UPSTREAM_URL, UPSTREAM_TIMEOUT_S


class HttpJson(Provider):
    async def generate(self, prompt: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=UPSTREAM_TIMEOUT_S) as client:
                r = await client.post(UPSTREAM_URL, json={"prompt": prompt})
                r.raise_for_status()
                data = r.json()
                text = data.get("text")
                if text is None:
                    raise HTTPException(
                        status_code=502, detail="Upstream missing 'text'"
                    )
                return str(text)
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Upstream timeout")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Upstream HTTP error: {e}")

    async def astream(self, prompt: str):
        # Non-streaming provider: implement later via chunker (Step 4)
        raise HTTPException(
            status_code=400, detail="Streaming not supported by http_json"
        )
