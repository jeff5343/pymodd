from pymodd.game import Game, Folder

from scripts import *
from entity_scripts import * 


class Froge(Game):
	def _build(self):
		self.entity_scripts = [Pooper(), Frog()]
		self.scripts = [
			Initialize(),
			PlayerJoins(),
			PlayerLeaves(),
			EverySecond(),
			WhenAUnitsAttributeBecomes0OrLess(),
			OpenShop(),
			
		]


# run `pymodd compile` within this project directory to generate this game's json files
# example:
"""
$ cd froge
$ pymodd compile
"""
