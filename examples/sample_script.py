from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Script, Trigger, write_to_output

from game import *


class EverySecond(Script):
    def __init__(self):
        self.triggers = [Trigger.EVERY_SECOND]
        self.actions = [
            IncreaseVariableByNumber(Variables.BOSS_TIMER, Number(1)),
            While(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG), '<', Number('5')), [
                CreateUnitForPlayerAtPosition(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), Number(0)),
            ]),
            IfStatement(Condition(Number(50), '<=', Variables.TIMER), [
                CreateUnitForPlayerAtPosition(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), Number(0)),
                SetVariable(Variables.TIMER, Number(0)),
                SendChatMessage(String('The frog boss has spawned!'))
            ]),
        ]
        # the order of the script in modd's project directory
        self.order = 1


# write the json for the script
write_to_output(EverySecond())
