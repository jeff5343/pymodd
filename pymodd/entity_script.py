from __future__ import annotations
import os
import inspect
from enum import Enum
from typing import Any, override

from pymodd.core.base import Base
from pymodd.core.script import Script

import pymodd.game
import pymodd.variable_types


class EntityScripts(pymodd.game.Game):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        # not calling super because Game loads JSON + holds EntityScripts
        self.entity_type: pymodd.variable_types.UnitTypeBase | None = None
        self.keybindings: dict[Key, KeyBehavior] = {}
        self.scripts: list[Any] = []
        self._build()
        # set position of scripts inside entity_scripts
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)


class KeyBehavior(Base):
    def __init__(
        self,
        key_down_script: Script | None = None,
        key_up_script: Script | None = None,
    ):
        # default values
        self.key_down_script_key, self.is_key_down_script_entity_script = "", False
        self.key_up_script_key, self.is_key_up_script_entity_script = "", False

        # update values if provided
        if key_down_script is not None:
            self.key_down_script_key = key_down_script.key
            sourcePath = inspect.getsourcefile(key_down_script.build_actions_function)
            # determine if it is a global script or an entity script
            if sourcePath is not None:
                self.is_key_down_script_entity_script = (
                    os.path.split(sourcePath)[-1] == "entity_scripts.py"
                )
        if key_up_script is not None:
            self.key_up_script_key = key_up_script.key
            sourcePath = inspect.getsourcefile(key_up_script.build_actions_function)
            if sourcePath is not None:
                self.is_key_up_script_entity_script = (
                    os.path.split(sourcePath)[-1] == "entity_scripts.py"
                )

    @override
    def to_dict(self, old_data: dict[str, Any] | None = None):
        # update the old data with new data if it is provided
        data = old_data if old_data is not None else self.get_template_data()
        data["keyDown"]["scriptName"] = self.key_down_script_key
        data["keyDown"]["isEntityScript"] = self.is_key_down_script_entity_script
        data["keyUp"]["scriptName"] = self.key_up_script_key
        data["keyUp"]["isEntityScript"] = self.is_key_up_script_entity_script
        return data

    def get_template_data(self) -> dict[str, Any]:
        return {
            "keyDown": {
                "scriptName": "",
                "isEntityScript": False,
                "cost": {},
            },
            "keyUp": {
                "scriptName": "",
                "isEntityScript": False,
                "cost": {},
            },
        }


class Key(Enum):
    LEFT_CLICK = "button1"
    RIGHT_CLICK = "button3"
    SPACE = "space"
    ENTER = "enter"
    ESCAPE = "escape"
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"
    F = "f"
    G = "g"
    H = "h"
    I = "i"
    J = "j"
    K = "k"
    L = "l"
    M = "m"
    N = "n"
    O = "o"
    P = "p"
    Q = "q"
    R = "r"
    S = "s"
    T = "t"
    U = "u"
    V = "v"
    W = "w"
    X = "x"
    Y = "y"
    Z = "z"
