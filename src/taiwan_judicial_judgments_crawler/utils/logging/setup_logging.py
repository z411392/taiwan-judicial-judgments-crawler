from logging import INFO, root, WARNING, getLogger, CRITICAL
from logging import StreamHandler


def setup_logging():
    root.setLevel(INFO)
    root.addHandler(StreamHandler())
    getLogger("vellox.utils.lifespan").setLevel(WARNING)
    getLogger("vellox.http").setLevel(WARNING)
    getLogger("werkzeug").setLevel(WARNING)
    getLogger("httpx").setLevel(WARNING)
    getLogger("opentelemetry").setLevel(CRITICAL + 1)
    getLogger("prefect").setLevel(CRITICAL + 1)
