import json
import random
import string
from enum import Enum

from caseconverter import camelcase, snakecase


class Base():
    def to_dict(self):
        raise NotImplementedError("to_dict method not implemented")


class Game(Base):
    def __init__(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        self.name = data.get('title')
        self.data = data
        self.entity_scripts = []
        self.scripts = []
        self._build()
        # set position of scripts inside game
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)

    def _build():
        pass

    def to_dict(self):
        # replace game scripts with scripts defined in self.scripts
        self.data['data']['scripts'] = self.flatten_scripts_data(self.scripts)
        for script in self.entity_scripts:
            entity_type_category, entity_type_id = f'{camelcase(script.entity_type.__class__.__name__)}s', script.entity_type_id
            self.data['data'][entity_type_category][entity_type_id]['scripts'] = self.flatten_scripts_data(
                script.scripts)
        return self.data

    def flatten_scripts_data(self, scripts):
        """Takes all scripts out of folders, transforms them into json, and put them all into one dictionary with the rest of the game's scripts

        Returns:
            dict: keys are the script's key, values are the script's data
        """
        flattened_scripts = {}
        scripts_queue = scripts.copy()
        while len(scripts_queue) > 0:
            script = scripts_queue.pop(0)
            # add folder's scripts to the queue
            if isinstance(script, Folder):
                scripts_queue += script.scripts
            script_data = script.to_dict()
            flattened_scripts[script_data['key']] = script_data
        return flattened_scripts

    def update_data_with_variable_classes(self, variable_classes):
        # pull variable objects out from each class
        variable_class_name_to_variables = {}
        for klass in variable_classes:
            class_name = klass.__name__
            variable_class_name_to_variables[class_name] = []
            class_vars = [item for item in vars(
                klass) if not item.startswith('_') and not callable(item)]
            for var in class_vars:
                variable_class_name_to_variables[class_name].append(getattr(
                    klass, var))

        # update game data with new variable objects
        for class_name, variables in variable_class_name_to_variables.items():
            variable_category_name = variable_category_name_from_variable_class_name(
                class_name)
            new_variables = filter(lambda variable: not self.variable_category_contains_variable(
                variable_category_name, variable), variables)
            for variable in new_variables:
                self.data['data'][variable_category_name][variable.id] = variable.get_template_data(
                )

    def variable_category_contains_variable(self, variable_category, variable):
        return variable.id in self.data['data'][variable_category].keys()


def variable_category_name_from_variable_class_name(variable_class_name):
    if variable_class_name == 'EntityVariables':
        return 'entityTypeVariables'
    elif variable_class_name == 'PlayerVariables':
        return 'playerTypeVariables'
    elif variable_class_name == 'Musics':
        return 'music'
    elif variable_class_name in ['Regions', 'ItemTypeGroups', 'UnitTypeGroups']:
        return 'variables'
    else:
        return camelcase(variable_class_name)


class EntityScripts(Game):
    def __init__(self):
        self.entity_type = None
        self.scripts = []
        self._build()
        # set position of scripts inside entity_scripts
        for i, script in enumerate(self.scripts):
            script.set_position(i, None)
        self.entity_type_id = self.get_entity_type_id()

    def get_entity_type_id(self):
        return self.entity_type.function.get('value')

    def to_dict(self):
        self.flatten_scripts_data(self.scripts)
        return self.data


class File(Base):
    def __init__(self):
        self.name = None
        self.key = None
        self.parent = None
        self.order = 0

    def set_position(self, order, parent):
        self.order = order
        self.parent = parent


class Folder(File):
    def __init__(self, name, scripts: list):
        super().__init__()
        self.name = name
        self.key = generate_random_key()
        self.scripts = scripts
        # set position of scripts inside the folder
        for i, script in enumerate(scripts):
            script.set_position(i, self.key)

    def to_dict(self):
        return {
            'key': self.key,
            'folderName': self.name,
            'parent': self.parent,
            'order': self.order,
            'expanded': True
        }


class Script(File):
    _class_to_key = {}

    def __new__(cls, *args, **kwargs):
        if cls._class_to_key.get(cls, None) is None:
            cls._class_to_key[cls] = generate_random_key()
        return super(Script, cls).__new__(cls, *args, **kwargs)

    def __init__(self):
        super().__init__()
        self.name = snakecase(self.__class__.__name__).replace('_', ' ')
        self.key = Script._class_to_key[self.__class__]
        self.triggers = []
        self.actions = []

    def _build(self):
        pass

    def to_dict(self):
        self._build()
        return {
            'triggers': [{'type': trigger.value} for trigger in self.triggers],
            'conditions': [{'operator': '==', 'operandType': 'boolean'}, True, True],
            'actions': self.actions,
            'name': self.name,
            'parent': self.parent,
            'key': self.key,
            'order': self.order
        }


def script(triggers=[], name=None):
    """
    Args:
        triggers (list, optional): triggers for the script. Defaults to [].
        name (str, optional): name to override the default name of the script. Defaults to the class name of the script.
    """
    def wrapper_script(cls):
        class NewScript(Script):
            def __init__(self):
                super().__init__()
                self.triggers = triggers
                if name is not None:
                    self.name = name
                else:
                    self.name = snakecase(cls.__name__).replace('_', ' ')

            def _build(self):
                cls._build(self)

        return NewScript
    return wrapper_script


def generate_random_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


def to_dict(obj):
    if isinstance(obj, Base):
        return obj.to_dict()
    if isinstance(obj, Enum):
        return obj.value
    return obj


# ---------------------------------------------------------------------------- #
#                                   Constants                                  #
# ---------------------------------------------------------------------------- #


class Trigger(Enum):
    GAME_START = 'gameStart'
    EVERY_FRAME = 'frameTick'
    EVERY_SECOND = 'secondTick'
    SERVER_SHUTTING_DOWN = 'serverShuttingDown'

    UNIT_TOUCHES_WALL = 'unitTouchesWall'
    UNIT_USES_ITEM = 'unitUsesItem'
    UNIT_ATTRIBUTE_BECOMES_ZERO = 'unitAttributeBecomesZero'
    UNIT_STARTS_USING_AN_ITEM = 'unitStartsUsingAnItem'
    UNIT_ATTRIBUTE_BECOMES_FULL = 'unitAttributeBecomesFull'
    UNIT_DROPPED_AN_ITEM = 'unitDroppedAnItem'
    UNIT_ENTERS_REGION = 'unitEntersRegion'
    UNIT_TOUCHES_ITEM = 'unitTouchesItem'
    UNIT_PICKED_AN_ITEM = 'unitPickedAnItem'
    UNIT_TOUCHES_UNIT = 'unitTouchesUnit'
    UNIT_TOUCHES_DEBRIS = 'unitTouchesDebris'
    UNIT_TOUCHES_PROJECTILE = 'unitTouchesProjectile'
    UNIT_STOPS_USING_AN_ITEM = 'unitStopsUsingAnItem'
    UNIT_ATTACKS_UNIT = 'unitAttacksUnit'
    UNIT_SELECTS_ITEM = 'unitSelectsItem'
    UNIT_SELECTS_INVENTORY_SLOT = 'unitSelectsInventorySlot'
    UNIT_ENTERS_SENSOR = 'unitEntersSensor'

    PROJECTILE_TOUCHES_ITEM = 'projectileTouchesItem'
    PROJECTILE_TOUCHES_DEBRIS = 'projectileTouchesDebris'
    PROJECTILE_ATTRIBUTE_BECOMES_ZERO = 'projectileAttributeBecomesZero'
    PROJECTILE_TOUCHES_WALL = 'projectileTouchesWall'
    PROJECTILE_ENTERS_SENSOR = 'projectileEntersSensor'

    PLAYER_CUSTOM_INPUT = 'playerCustomInput'
    PLAYER_ATTRIBUTE_BECOMES_FULL = 'playerAttributeBecomesFull'
    PLAYER_JOINS_GAME = 'playerJoinsGame'
    PLAYER_PURCHASES_UNIT = 'playerPurchasesUnit'
    PLAYER_LEAVES_GAME = 'playerLeavesGame'
    PLAYER_ATTRIBUTE_BECOMES_ZERO = 'playerAttributeBecomesZero'
    PLAYER_SENDS_CHAT_MESSAGE = 'playerSendsChatMessage'

    ITEM_ATTRIBUTE_BECOMES_FULL = 'itemAttributeBecomesFull'
    ITEM_ENTERS_REGION = 'itemEntersRegion'
    ITEM_TOUCHES_WALL = 'itemTouchesWall'
    ITEM_ATTRIBUTE_BECOMES_ZERO = 'itemAttributeBecomesZero'
    ITEM_IS_USED = 'itemIsUsed'
    ITEM_ENTERS_SENSOR = 'itemEntersSensor'
    RAYCAST_ITEM_FIRED = 'raycastItemFired'

    ENTITY_CREATED = 'entityCreated'
    ENTITY_TOUCHES_WALL = 'entityTouchesWall'
    ENTITY_TOUCHES_ITEM = 'entityTouchesItem'
    ENTITY_TOUCHES_UNIT = 'entityTouchesUnit'
    ENTITY_TOUCHES_PROJECTILE = 'entityTouchesProjectile'
    ENTITY_ATTRIBUTE_BECOMES_ZERO = 'entityAttributeBecomesZero'
    ENTITY_ATTRIBUTE_BECOMES_FULL = 'entityAttributeBecomesFull'
    ENTITY_ENTERS_REGION = 'entityEntersRegion'
    ENTITY_GETS_ATTACKED = 'entityGetsAttacked'

    DEBRIS_ENTERS_REGION = 'debrisEntersRegion'

    AD_PLAY_COMPLETED = 'adPlayCompleted'
    AD_PLAY_SKIPPED = 'adPlaySkipped'
    AD_PLAY_FAILED = 'adPlayFailed'
    AD_PLAY_BLOCKED = 'adPlayBlocked'

    SEND_COINS_SUCCESS = 'sendCoinsSuccess'
    COIN_SEND_FAILURE_DUE_TO_DAILY_LIMIT = 'coinSendFailureDueToDailyLimit'
    COIN_SEND_FAILURE_DUE_TO_INSUFFICIENT_COINS = 'coinSendFailureDueToInsufficientCoins'


class UiTarget(Enum):
    TOP = 'top'
    CENTER = 'center-lg'
    SCOREBOARD = 'scoreboard'


class Flip(Enum):
    NONE = 'none'
    HORIZONTAL = 'horizontal'
    VERTICAL = 'vertical'
    BOTH = 'both'
