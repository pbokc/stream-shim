import json
import httpx
from fastapi import HTTPException
from typing import AsyncIterator, List, Dict
from .provider import Provider
from config import UPSTREAM_TIMEOUT_S

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


class Ollama(Provider):
    def _format_messages(self, prompt: str) -> List[Dict[str, str]]:
        # Simple MVP: send the whole prompt as a single user message
        return [{"role": "user", "content": prompt}]

    async def generate(self, prompt: str) -> str:
        # Accumulate streaming chunks
        chunks = []
        async for part in self.astream(prompt):
            chunks.append(part)
        return "".join(chunks)

    async def astream(self, prompt: str) -> AsyncIterator[str]:
        payload = {
            "model": "mistral",  # change via env later if you like
            "messages": self._format_messages(prompt),
            "stream": True,
        }
        try:
            async with httpx.AsyncClient(timeout=UPSTREAM_TIMEOUT_S) as client:
                async with client.stream("POST", OLLAMA_URL, json=payload) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        # Ollama streams JSON per line; each has {"message":{"content":"..."}} or {"done":true}
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            # Ignore keepalives or malformed lines
                            continue
                        if obj.get("done"):
                            break
                        msg = obj.get("message") or {}
                        content = msg.get("content")
                        if content:
                            yield content
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Ollama timeout")
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Ollama HTTP error: {e}")
