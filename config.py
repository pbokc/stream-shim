import os
from dotenv import load_dotenv

# Load .env file automatically
load_dotenv()

# Server binding
BIND_HOST = os.getenv("BIND_HOST", "127.0.0.1")
BIND_PORT = int(os.getenv("BIND_PORT", "8000"))

# Upstream provider config
PROVIDER_TYPE = os.getenv("PROVIDER_TYPE", "http_json")
UPSTREAM_URL = os.getenv("UPSTREAM_URL", "http://127.0.0.1:5001/generate")

# Timeouts and chunking
UPSTREAM_TIMEOUT_S = int(os.getenv("UPSTREAM_TIMEOUT_S", "30"))
CHUNK_MODE = os.getenv("CHUNK_MODE", "word")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "3"))
MIN_DELAY_MS = int(os.getenv("MIN_DELAY_MS", "20"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
