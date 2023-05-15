from pymodd.game import Folder
from pymodd.entity_script import EntityScripts, Key, KeyBehavior

from scripts import *


class Pooper(EntityScripts):
	def _build(self):
		self.entity_type = UnitTypes.POOPER
		self.keybindings = {
			Key.LEFT_CLICK: KeyBehavior(self.UseItem(), self.StopUsingItem()),
			Key.A: KeyBehavior(self.UseItem(), EverySecond()),
			Key.B: KeyBehavior(OpenShop(), None),
			
		}
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
		self.keybindings = {
			
		}
		self.scripts = [
			self.NewScript(),
			
		]

	@script(triggers=[])
	class NewScript():
		def _build(self):
			comment('wdwadawd')


