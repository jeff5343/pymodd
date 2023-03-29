from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import EntityScripts, Folder, Script, Trigger, UiTarget, Flip

from game_variables import *


class Pooper(EntityScripts):
	def _build(self):
		self.entity_type = UnitTypes.POOPER
		self.scripts = [
			self.UseItem(),
			self.StopUsingItem(),
			
		]

	class UseItem(Script):
		def _build(self):
			self.key = 'umIqJLd7De'
			self.triggers = []
			self.actions = [
				use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(ThisEntity())),
				
			]

	class StopUsingItem(Script):
		def _build(self):
			self.key = 'OJ9Po4VSQg'
			self.triggers = []
			self.actions = [
				stop_using_item(ItemCurrentlyHeldByUnit(ThisEntity())),
				
			]


class Frog(EntityScripts):
	def _build(self):
		self.entity_type = UnitTypes.FROG
		self.scripts = [
			self.NewScript(),
			
		]

	class NewScript(Script):
		def _build(self):
			self.key = 'XUAEBhSryo'
			self.triggers = []
			self.actions = [
				comment('wdwadawd'),
				
			]


