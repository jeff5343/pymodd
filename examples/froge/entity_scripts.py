from pymodd.core.folder import Folder
from pymodd.entity_script import EntityScripts, Key, KeyBehavior

from scripts import *


class User(EntityScripts):
    def _build(self):
        self.entity_type = UnitType.USER
        self.keybindings = {
            Key.LEFT_CLICK: KeyBehavior(self.use_item(), self.stop_using_item()),
            Key.B: KeyBehavior(open_shop(), None),
            
        }
        self.scripts = [
            self.use_item(),
            self.stop_using_item(),
            
        ]

    @script(triggers=[])
    def use_item():
        use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(ThisEntity()))

    @script(triggers=[])
    def stop_using_item():
        stop_using_item(ItemCurrentlyHeldByUnit(ThisEntity()))


class Frog(EntityScripts):
    def _build(self):
        self.entity_type = UnitType.FROG
        self.keybindings = {
            
        }
        self.scripts = [
            self.new_script(),
            
        ]

    @script(triggers=[])
    def new_script():
        comment('wdwadawd')


