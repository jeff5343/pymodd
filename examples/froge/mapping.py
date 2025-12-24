from pymodd.game import Game
from pymodd.core.folder import Folder

from scripts import *
from entity_scripts import * 


class Froge(Game):
    def _build(self):
        self.entity_scripts = [User(), Frog()]
        self.scripts = [
            initialize(),
            player_joins(),
            player_leaves(),
            every_second(),
            when_a_units_attribute_becomes_0_or_less(),
            open_shop(),
            
        ]


# run `pymodd compile` within this project directory to generate this game's json files
# example:
"""
$ cd froge
$ pymodd compile
"""
