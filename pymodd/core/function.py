from typing import Any, override

from pymodd.core.base import Base


class Function(Base):
    """
    The base class for all functions in pymodd.
    """

    def __init__(self):
        self.function: str | dict[str, Any] | None = None
        self.options: dict[str, Any] = {}

    @override
    def to_dict(self):
        # check for direct values (Number, Boolean, String)
        if type(self.function) is dict and self.function.get("direct"):
            return self.function.get("value")

        data = {"function": self.function}
        if self.options is not None:
            data.update(self.options)
        return data

    # removes lsp warnings
    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __eq__(self, other):
        return True

    def __lt__(self, other):
        return True

    def __le__(self, other):
        return True

    # removes lsp warnings
    def __iter__(self):
        return iter([])

    def __next__(self):
        return iter([]).__next__
