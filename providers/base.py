from typing import AsyncIterator


class Provider:
    async def generate(self, prompt: str) -> str:
        """Return full text completion."""
        raise NotImplementedError

    async def astream(self, prompt: str) -> AsyncIterator[str]:
        """Yield text chunks (for streaming-capable providers)."""
        raise NotImplementedError
