from pymodd.script import Game, Folder, write_game_to_output, write_to_output

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

# run `python froge/mapping.py` to generate this game's files
write_game_to_output(Froge('froge/utils/game.json'))
# uncomment the following to quickly generate the json file for a script
# write_to_output('output/', SCRIPT_OBJECT())