from enum import Enum
from typing import Any

from pymodd.core.base import Base


def to_dict(obj: Any) -> Any:
    """
    Util function to convert any object into a dict/JSON acceptable value
    """
    if isinstance(obj, Base):
        return obj.to_dict()
    if isinstance(obj, Enum):
        return obj.value
    return obj
