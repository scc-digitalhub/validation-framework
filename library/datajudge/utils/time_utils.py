from datetime import datetime


def get_time() -> str:
    """Return string of datetime.now()."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
