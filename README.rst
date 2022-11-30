Pymodd
======

Pymodd is a python package allowing for the creation of modd.io games in python!

Features
-----------------------

- generate modd.io scripts with python
- more coming soon?

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
        def __init__(self):
            self.triggers = [Trigger.EVERY_SECOND]
            self.actions = [
                IncreaseVariableByNumber(Variables.BOSS_TIMER, 1),
                While(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG), '<', 5), [
                    CreateUnitForPlayerAtPosition(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
                ])
            ]
            self.order = 1

    write_to_output(EverySecond())