========================
pymodd library validator
========================

generates the content of new triggers, actions, and functions for copy-pasting directly into pymodd.

internally compares the triggers, actions, and functions implemented in pymodd with the triggers, actions, and functions fetched from the modd.io editor api in order to determine what needs to be generated.

Requirements
------------

rust (`install <https://www.rust-lang.org/tools/install>`_)


How to Run
----------

.. code:: sh

    # go into this directory
    cd pymodd_library_validator
    # run the project
    cargo run

Output
------

up to three files may be generated

- ``new_triggers.py`` if any new triggers are detected
    insert generated trigger enums inside the ``Trigger`` class located within ``pymodd/script.py``

- ``new_actions.py`` if any new actions are detected
    insert geneerated action functions inside ``pymodd/actions.py``

- ``new_functions.py`` if any new functions are detected
    insert generated function classes under their correct commented categories located inside ``pymodd/functions.py``