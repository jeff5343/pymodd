import os
import json
from enum import Enum

from .utils.data_templates import SCRIPT_DATA_TEMPLATE


def write_to_output(obj):
    if not os.path.isdir('output/'): os.mkdir('output/')
    file_name = f'{obj.__class__.__name__}.json'
    with open(f'output/{file_name}', 'w') as output:
        output.write(json.dumps(obj.to_dict()))
        print(f'{file_name} was successfuly created in the output folder')


class Base():
    def to_dict(self):
        raise NotImplementedError("to_dict method not implemented")


class Script(Base):
    def __init__(self):
        self.triggers = []
        self.actions = []
        self.order = 0

    def to_dict(self):
        data = SCRIPT_DATA_TEMPLATE
        data['triggers'] = [{'type': trigger.value}
                            for trigger in self.triggers]
        data['actions'] = [action.to_dict() for action in self.actions]
        data['name'] = self.__class__.__name__
        data['order'] = self.order
        return data


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

    DEBRIS_ENTERS_REGION = 'debrisEntersRegion'
