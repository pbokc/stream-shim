from fastapi import FastAPI
from typing import List
from schemas import ChatCompletionRequest, ChatMessage

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
    # Simple MVP formatting: refine later if needed
    parts = [f"{m.role}: {m.content}" for m in messages]
    return "\n".join(parts)


@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    prompt = join_messages(req.messages)
    # Stub response (no provider yet): echo parsed prompt
    return {
        "id": "stub-0001",
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": f"(echo) {prompt}"},
                "finish_reason": "stop",
            }
        ],
        "model": req.model,
    }
