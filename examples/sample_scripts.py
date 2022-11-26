from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Script, Trigger, write_to_output

from game import *


class EverySecond(Script):
    def __init__(self):
        self.triggers = [Trigger.EVERY_SECOND]
        self.actions = [
            IncreaseVariableByNumber(Variables.BOSS_TIMER, 1),
            While(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG), '<', '5'), [
                CreateUnitForPlayerAtPosition(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
            ]),
            IfStatement(Condition(50, '<=', Variables.TIMER), [
                CreateUnitForPlayerAtPosition(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
                SetVariable(Variables.TIMER, 0),
                SendChatMessage('The frog boss has spawned!')
            ]),
        ]
        # the order of the script in modd's project directory
        self.order = 1


# write the json for the script
write_to_output(EverySecond())
