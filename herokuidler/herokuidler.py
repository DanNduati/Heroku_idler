from typing import Any, Dict, NamedTuple


class CurrentUrl(NamedTuple):
    todo: Dict[str, Any]
    error: int
