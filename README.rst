Pymodd
======

Pymodd is a python package for creating modd.io games in python!

Features
-----------------------

- mapping file for organizing scripts
- edit global scripts and entity scripts
- command to generate a pymodd project

Installing
-----------------------

**Python 3.8 or higher is required**

To install the library run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U pymodd

    # Windows
    py -3 -m pip install -U pymodd


Getting Started
-----------------------

Export your modd game json file from the website and then generate a project by running this command:

.. code:: sh

    generate-game {PATH TO GAME JSON FILE}


Quick Script Example
-----------------------

view examples/sample_scripts.py in the github repo for the full example

.. code:: py

	class EverySecond(Script):
		def _build(self):
			self.key = 'P8MwXcSxq7'
			self.triggers = [Trigger.EVERY_SECOND]
			self.actions = [
				IfStatement(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG), '<', 5), [
					CreateUnitForPlayerAtPosition(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
				], [
					IfStatement(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG_BOSS), '==', 0), [
						IfStatement(Condition(Variables.BOSS_TIMER, '<=', 0), [
							CreateUnitForPlayerAtPosition(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
							UpdateUiTextForTimeForPlayer(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000),
						], [
						]),
						DecreaseVariableByNumber(Variables.BOSS_TIMER, 1),
					], [
					]),
				]),
			]
