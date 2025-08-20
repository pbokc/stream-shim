from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("🚀 Starting stream-shim")

@app.get("/")
async def root():
    return {"service": "stream-shim", "status": "running"}

@app.get("/healthz")
async def read_healthz():
    return {"status":"ok"}