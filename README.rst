======
pymodd
======

|Build| |Version| |License|

pymodd is a python package for creating and editing modd.io games in python

.. |Build| image:: https://img.shields.io/github/actions/workflow/status/jeff5343/pymodd/test.yml?label=CI&logo=github&style=plastic
   :alt: GitHub Workflow Status
.. |Version| image:: https://img.shields.io/pypi/v/pymodd?style=plastic
   :alt: PyPI
.. |License| image:: https://img.shields.io/pypi/l/pymodd?style=plastic
   :alt: PyPI - License

Features
--------

- edit global and entity scripts
- organize folders and scripts with a mapping file
- edit environment variables
- a command to generate and compile a pymodd project

Documentation
-------------

The pymodd wiki is located at `github.com/jeff5343/pymodd/wiki <https://github.com/jeff5343/pymodd/wiki>`_

A brief outline:

- `Introduction <https://github.com/jeff5343/pymodd/wiki>`_
- `Install Guide <https://github.com/jeff5343/pymodd/wiki/Install-Guide>`_
- `Generating and Compiling a Pymodd Project <https://github.com/jeff5343/pymodd/wiki/Generating-and-Compiling-a-Pymodd-Project>`_
- `Pymodd Project Structure <https://github.com/jeff5343/pymodd/wiki/Pymodd-Project-Structure>`_


Quick Script Example
--------------------

view the ``examples/froge`` directory in the `github repository <https://github.com/jeff5343/pymodd>`_ to view the entire pymodd project

.. code:: py

    @script(triggers=[Trigger.EVERY_SECOND])
    def every_second():
        if NumberOfUnitsOfUnitType(UnitType.FROG) < 5:
            create_unit_for_player_at_position_with_rotation(UnitType.FROG, Variable.AI, RandomPositionInRegion(EntireMapRegion()), 0)
        else:
            if NumberOfUnitsOfUnitType(UnitType.FROG_BOSS) == 0:
                if Variable.BOSS_TIMER <= 0:
                    create_unit_for_player_at_position_with_rotation(UnitType.FROG_BOSS, Variable.AI, RandomPositionInRegion(EntireMapRegion()), 0)
                    update_ui_target_for_player_for_miliseconds(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000)
                decrease_variable_by_number(Variable.BOSS_TIMER, 1)

