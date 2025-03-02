from datetime import UTC, datetime
from typing import NoReturn


def utc_now() -> datetime:
    return datetime.now(UTC)


def raise_(msg: str) -> NoReturn:
    raise RuntimeError(msg)


MM_JINJA_GLOBALS = {
    "raise": raise_,
    "utc_now": utc_now,
}
