from langchain.tools import tool


@tool
def get_current_time() -> str:
    """Return the current UTC time."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
