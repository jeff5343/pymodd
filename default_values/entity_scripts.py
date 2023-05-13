from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import EntityScripts, Folder, Trigger, UiTarget, Flip, script

from game_variables import *


class Pooper(EntityScripts):
	def _build(self):
		self.entity_type = UnitTypes.POOPER
		self.scripts = [
			self.UseItem(),
			self.StopUsingItem(),
			
		]

	@script(triggers=[])
	class UseItem():
		def _build(self):
			use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(ThisEntity()))

	@script(triggers=[])
	class StopUsingItem():
		def _build(self):
			stop_using_item(ItemCurrentlyHeldByUnit(ThisEntity()))


class Frog(EntityScripts):
	def _build(self):
		self.entity_type = UnitTypes.FROG
		self.scripts = [
			self.NewScript(),
			
		]

	@script(triggers=[])
	class NewScript():
		def _build(self):
			comment('wdwadawd')


