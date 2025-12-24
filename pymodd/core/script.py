from typing import Any, override
from pymodd.utils.generate_random_key import generate_random_key

from .file import File


class Script(File):
    # this dict maps classes by calling id() (memory addresses)
    # this works because one new NewScript class is created for each @script decorator
    _class_to_key: dict[type, str] = {}

    def __new__(cls, *args, **kwargs):
        if cls._class_to_key.get(cls, None) is None:
            cls._class_to_key[cls] = generate_random_key()
        return super(Script, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()
        self.name: str | None = None
        self.key: str | None = Script._class_to_key[self.__class__]
        self.triggers = []
        self.actions = []
        self.build_actions_function = lambda *args, **kwargs: None

    def to_dict(self, project_globals_data: dict[str, Any] = {}):
        return super().to_dict()
