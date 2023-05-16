import os
import inspect
from enum import Enum

from pymodd.game import Base, Game


class EntityScripts(Game):
    def __init__(self):
        self.entity_type = None
        self.keybindings = {}  # dict of Keys to KeyBehavior
        self.scripts = []
        self._build()
        # set position of scripts inside entity_scripts
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)


class KeyBehavior(Base):
    def __init__(self, key_down_script=None, key_up_script=None):
        self.key_down_script_key, self.is_key_down_script_entity_script = "", False
        self.key_up_script_key, self.is_key_up_script_entity_script = "", False
        if key_down_script is not None:
            self.key_down_script_key = key_down_script.key
            self.is_key_down_script_entity_script = os.path.split(
                inspect.getsourcefile(key_down_script.build_actions_function))[-1] == 'entity_scripts.py'
        if key_up_script is not None:
            self.key_up_script_key = key_up_script.key
            self.is_key_up_script_entity_script = os.path.split(
                inspect.getsourcefile(key_up_script.build_actions_function))[-1] == 'entity_scripts.py'

    def to_dict(self, old_data: None):
        # update the old data with new data if it is provided
        data = old_data if old_data is not None else self.get_template_data()
        data['keyDown']['scriptName'] = self.key_down_script_key
        data['keyDown']['isEntityScript'] = self.is_key_down_script_entity_script
        data['keyUp']['scriptName'] = self.key_up_script_key
        data['keyUp']['isEntityScript'] = self.is_key_up_script_entity_script
        return data

    def get_template_data(self):
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
            }
        }


class Key(Enum):
    LEFT_CLICK = 'button1'
    RIGHT_CLICK = 'button3'
    SPACE = 'space'
    ENTER = 'enter'
    ESCAPE = 'escape'
    UP = 'up'
    DOWN = 'down'
    RIGHT = 'right'
    LEFT = 'left'
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'
