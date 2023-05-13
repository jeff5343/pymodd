from pymodd.script import Game, Folder

from scripts import *
from entity_scripts import * 


class DefaultValues(Game):
	def _build(self):
		self.entity_scripts = [Pooper(), Frog()]
		self.scripts = [
			Initialize(),
			PlayerJoins(),
			PlayerLeaves(),
			EverySecond(),
			WhenAunitsAttributeBecomes0orLess(),
			OpenShop(),
			
		]


# run `pymodd compile` within this project directory to generate this game's json files
# example:
"""
$ cd default_values
$ pymodd compile
"""
