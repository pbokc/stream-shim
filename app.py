from fastapi import FastAPI
from typing import List
from schemas import ChatCompletionRequest, ChatMessage
from providers.factory import get_provider

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("🚀 Starting stream-shim")


@app.get("/")
async def root():
    return {"service": "stream-shim", "status": "running"}


@app.get("/healthz")
async def read_healthz():
    return {"status": "ok"}


def join_messages(messages: List[ChatMessage]) -> str:
    return "\n".join(f"{m.role}: {m.content}" for m in messages)


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    provider = get_provider()
    prompt = join_messages(req.messages)
    # Step 3: call provider.generate (non-streaming response)
    text = await provider.generate(prompt)
    return {
        "id": "cmp-0001",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": text},
                "finish_reason": "stop",
            }
        ],
        "model": req.model,
    }
