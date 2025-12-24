from typing import override
from pymodd.utils.generate_random_key import generate_random_key

from .file import File


class Folder(File):
    def __init__(self, name: str, scripts: list[File]):
        super().__init__()
        self.name: str | None = name
        self.key: str | None = generate_random_key()
        self.scripts: list[File] = scripts
        # set position of scripts inside the folder
        for i, script in enumerate(scripts):
            script.set_position(i, self.key)

    @override
    def to_dict(self) -> dict[str, str | int | bool | None]:
        return {
            "key": self.key,
            "folderName": self.name,
            "parent": self.parent,
            "order": self.order,
            "expanded": True,
        }
