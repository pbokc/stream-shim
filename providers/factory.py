from config import PROVIDER_TYPE


def get_provider():
    if PROVIDER_TYPE == "http_json":
        from .http_json import HttpJson

        return HttpJson()
    if PROVIDER_TYPE == "ollama":
        from .ollama import Ollama

        return Ollama()
    raise ValueError(f"Unknown PROVIDER_TYPE: {PROVIDER_TYPE}")
