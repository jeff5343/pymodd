from .base import Base


class File(Base):
    """
    The base class for all directory items in pymodd (Folder, Script).
    """

    def __init__(self) -> None:
        self.name: str | None = None
        self.key: str | None = None
        self.parent: str | None = None
        self.order: int = 0

    def set_position(self, order: int, parent: str | None):
        self.order = order
        self.parent = parent
