from enum import Enum

import pymodd

from pymodd.script import generate_random_key
from pymodd.functions import Function


class VariableType(Function):
    def __init__(self, id=None, **data_keys_to_new_values_kwargs):
        self.id = generate_random_key() if id is None else id
        self.data_keys_to_new_values = data_keys_to_new_values_kwargs.items()
        self.function = {
            'direct': True,
            'value': self.id,
        }

    def updated_data_with_user_provided_values(self, data):
        for key, value in self.data_keys_to_new_values:
            if key in data.keys():
                data[key] = value
        return data

    def get_template_data(self) -> dict:
        raise NotImplementedError('_get_template_data method not implemented')


class DataType(Enum):
    NUMBER = 'number'
    STRING = 'string'
    BOOLEAN = 'boolean'
    ITEM = 'item'
    UNIT = 'unit'
    PLAYER = 'player'
    PROJECTILE = 'projectile'
    ITEM_TYPE = 'itemType'
    UNIT_TYPE = 'unitType'
    PLAYER_TYPE = 'playerType'
    PROJECTILE_TYPE = 'projectileType'
    ITEM_GROUP = 'itemGroup'
    UNIT_GROUP = 'unitGroup'
    PLAYER_GROUP = 'playerGroup'
    ITEM_TYPE_GROUP = 'itemTypeGroup'
    UNIT_TYPE_GROUP = 'unitTypeGroup'
    REGION = 'region'


class VariableBase(VariableType):
    def __init__(self, variable_name, data_type: DataType, default_value=None):
        super().__init__(variable_name)
        self.data_type = data_type
        self.default_value = default_value
        self.function = 'getVariable'
        self.options = {
            'variableName': variable_name,
        }

        if default_value is not None:
            # group types take in a list of types as their default values
            if data_type in [DataType.ITEM_TYPE_GROUP, DataType.UNIT_TYPE_GROUP] and type(default_value) is list:
                # convert the list of types into modd.io data
                self.default_value = {}
                for type_ in default_value:
                    id = type_.id if isinstance(
                        type_, (ItemTypeBase, UnitTypeBase)) else type_
                    self.default_value[id] = {
                        'probability': 20,
                        'quantity': 1
                    }
            # regions have additional parameters for their default value (currently not supported)
            if data_type == DataType.REGION:
                self.default_value = {
                    'x': 0,
                    'y': 0,
                    'width': 100,
                    'height': 100,
                    'inside': '#FFFFFF',
                    'outside': '',
                    'alpha': 100,
                    'videoChatEnabled': False
                }

    def updated_data_with_user_provided_values(self, data):
        data = super().updated_data_with_user_provided_values(data)
        if self.default_value is not None:
            data['default'] = self.default_value
        return data

    def get_template_data(self):
        return {
            'dataType': f'{self.data_type.value}',
            'default': self.default_value if self.default_value is not None else None
        }

    def _get_iterating_action(self):
        '''For group data types only. Used during script compilation'''
        if self.data_type == DataType.ITEM_GROUP:
            return pymodd.functions.ItemGroup()._get_iterating_action()
        elif self.data_type == DataType.UNIT_GROUP:
            return pymodd.functions.UnitGroup()._get_iterating_action()
        elif self.data_type == DataType.PLAYER_GROUP:
            return pymodd.functions.PlayerGroup()._get_iterating_action()
        elif self.data_type == DataType.ITEM_TYPE_GROUP:
            return pymodd.functions.ItemTypeGroup()._get_iterating_action()
        elif self.data_type == DataType.UNIT_TYPE_GROUP:
            return pymodd.functions.UnitTypeGroup()._get_iterating_action()
        return None

    def _get_iteration_object(self):
        '''For group data types only. Used during script compilation'''
        if self.data_type == DataType.ITEM_GROUP:
            return pymodd.functions.ItemGroup()._get_iteration_object()
        elif self.data_type == DataType.UNIT_GROUP:
            return pymodd.functions.UnitGroup()._get_iteration_object()
        elif self.data_type == DataType.PLAYER_GROUP:
            return pymodd.functions.PlayerGroup()._get_iteration_object()
        elif self.data_type == DataType.ITEM_TYPE_GROUP:
            return pymodd.functions.ItemTypeGroup()._get_iteration_object()
        elif self.data_type == DataType.UNIT_TYPE_GROUP:
            return pymodd.functions.UnitTypeGroup()._get_iteration_object()
        return None


class EntityVariableBase(VariableBase):
    def __init__(self, variable_name, data_type):
        super().__init__(variable_name, data_type)
        self.function = 'getEntityVariable'
        self.options = {
            'variable': {
                'text': f'{variable_name}',
                'dataType': f'{data_type.value}',
                'entity': 'null',
                'key': f'{variable_name}'
            }
        }


class PlayerVariableBase(VariableBase):
    def __init__(self, variable_name, data_type):
        super().__init__(variable_name, data_type)
        self.function = 'getPlayerVariable'
        self.options = {
            'variable': {
                'text': f'{variable_name}',
                'dataType': f'{data_type.value}',
                'entity': 'null',
                'key': f'{variable_name}'
            }
        }


class UnitTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'backpackSize': 0,
            'defaultItem': [],
            'controls': {
                'permittedInventorySlots': [],
                'movementMethod': 'velocity',
                'movementControlScheme': 'wasd',
                'abilities': {
                    'movementWheel': {
                        'mobilePosition': {
                            'y': 204,
                            'x': 35
                        }
                    },
                    'lookWheel': {
                        'mobilePosition': {
                            'y': 204,
                            'x': 407
                        }
                    },
                    'e': {
                        'keyUp': {
                            'scriptName': '',
                            'cost': {}
                        },
                        'keyDown': {
                            'scriptName': 'w2VrnZHyom',
                            'cost': {},
                            'isEntityScript': True
                        }
                    },
                    'g': {
                        'keyUp': {
                            'scriptName': '',
                            'cost': {}
                        },
                        'keyDown': {
                            'scriptName': 'yP67J1MMRN',
                            'cost': {},
                            'isEntityScript': True
                        }
                    },
                    'button1': {
                        'keyUp': {
                            'scriptName': 'DOrbWp0AGz',
                            'cost': {},
                            'isEntityScript': True
                        },
                        'keyDown': {
                            'scriptName': 'YFeMQ20gBX',
                            'cost': {},
                            'isEntityScript': True
                        }
                    }
                },
                'mouseBehaviour': {
                    'flipSpriteHorizontallyWRTMouse': False,
                    'rotateToFaceMouseCursor': True
                },
                'movementType': 'wasd',
                'absoluteRotation': False
            },
            'inventoryImage': '',
            'animations': {
                'default': {
                    'name': 'default',
                    'frames': [
                        1
                    ],
                    'loopCount': 0,
                    'framesPerSecond': 0
                }
            },
            'canBePurchasedBy': [],
            'isPurchasable': False,
            'states': {
                'default': {
                    'name': 'default',
                    'sound': {},
                    'particles': {},
                    'animation': 'default',
                    'body': 'default'
                }
            },
            'sound': {
                'KK9JlU1UQy': {
                    'name': 'Cough',
                    'file': 'https://modd.s3.amazonaws.com/asset/sound/1517554516253_man_cough.mp3'
                },
                'fEhDyJ8knx': {
                    'name': 'Scream',
                    'file': 'https://modd.s3.amazonaws.com/asset/sound/1517556903046_man_scream1.mp3'
                }
            },
            'particles': {},
            'body': {
                'spriteScale': 1,
                'fixtures': [
                    {
                        'shape': {
                            'type': 'rectangle'
                        },
                        'restitution': 0.01,
                        'friction': 0.01,
                        'density': 3
                    }
                ],
                'isFlying': False,
                'fixedRotation': False,
                'constantSpeed +DestroyedOnCollisionWithWall/unit': False,
                'allowSleep': True,
                'angularDamping': 1,
                'linearDamping': 5,
                'rotationSpeed': 2,
                'type': 'dynamic',
                'height': 40,
                'width': 40,
                'collidesWith': {
                    'units': True,
                    'items': True,
                    'projectiles': True,
                    'walls': True,
                    'unit': True,
                    'item': True,
                    'debris': True
                },
                'z-index': {
                    'layer': 3,
                    'depth': 3
                },
                'name': 'Human-body'
            },
            'spawnPosition': {
                'y': 2200,
                'x': 1500
            },
            'attributes': {
                'speed': {
                    'decimalPlaces': 0,
                    'dataType': '',
                    'name': 'speed',
                    'min': 0,
                    'max': 200,
                    'value': 10,
                    'regenerateSpeed': 0,
                    'isVisible': [],
                    'showAsHUD': True,
                    'color': '#00fff0',
                    'displayValue': True
                },
                'health': {
                    'decimalPlaces': 0,
                    'color': '#ffff0f',
                    'showAsHUD': True,
                    'displayValue': True,
                    'isVisible': [
                        'centerBar'
                    ],
                    'regenerateSpeed': 0,
                    'value': 100,
                    'dataType': '',
                    'max': 100,
                    'min': 0,
                    'name': 'health '
                }
            },
            'abilities': {
                'movementWheel': {
                    'mobilePosition': {
                        'y': 204,
                        'x': 35
                    }
                },
                'lookWheel': {
                    'mobilePosition': {
                        'y': 204,
                        'x': 407
                    }
                },
                'w': {
                    'keyUp': 'stopMovingUp',
                    'keyDown': 'moveUp'
                },
                'a': {
                    'keyUp': 'stopMovingLeft',
                    'keyDown': 'moveLeft'
                },
                's': {
                    'keyUp': 'stopMovingDown',
                    'keyDown': 'moveDown'
                },
                'd': {
                    'keyUp': 'stopMovingRight',
                    'keyDown': 'moveRight'
                },
                'button1': {
                    'keyUp': 'stopUsingItem',
                    'keyDown': 'startUsingItem',
                    'mobilePosition': {
                        'x': 326,
                        'y': 132
                    }
                },
                'up': {
                    'keyUp': 'stopMovingUp',
                    'keyDown': 'moveUp'
                },
                'down': {
                    'keyUp': 'stopMovingDown',
                    'keyDown': 'moveDown'
                },
                'left': {
                    'keyUp': 'stopMovingLeft',
                    'keyDown': 'moveLeft'
                },
                'right': {
                    'keyUp': 'stopMovingRight',
                    'keyDown': 'moveRight'
                },
                'e': {
                    'keyUp': '',
                    'keyDown': 'pickUp',
                    'mobilePosition': {
                        'x': 366,
                        'y': 85
                    }
                },
                'f': {
                    'keyUp': '',
                    'keyDown': 'pickUp'
                },
                'g': {
                    'keyUp': '',
                    'keyDown': 'drop',
                    'mobilePosition': {
                        'x': 365,
                        'y': 33
                    }
                },
                'b': {
                    'keyUp': '',
                    'keyDown': 'shop',
                    'mobilePosition': {
                        'x': 419,
                        'y': 32
                    }
                }
            },
            'baseSpeed': 53,
            'price': {},
            'skin': 'https://s3-us-west-1.amazonaws.com/modd/halloween-0.18/spritesheet/man.png',
            'canBuyItem': True,
            'handle': 'human',
            'name': 'New Unit Type',
            'inventorySize': 5,
            'cellSheet': {
                'url': 'https://cache.modd.io/asset/spriteImage/1588303353803_Human Circle Person.png',
                'rowCount': 1,
                'columnCount': 1
            },
            'bodies': {
                'default': {
                    'bullet': False,
                    'name': 'default',
                    'type': 'dynamic',
                    'width': 54,
                    'height': 54,
                    'z-index': {
                        'layer': 3,
                        'depth': 3
                    },
                    'fixedRotation': False,
                    'constantSpeed +DestroyedOnCollisionWithWall/unit': False,
                    'allowSleep': True,
                    'collidesWith': {
                        'units': True,
                        'items': True,
                        'projectiles': True,
                        'walls': True,
                        'debris': True
                    },
                    'angularDamping': 1,
                    'linearDamping': 8,
                    'rotationSpeed': 1,
                    'spriteScale': 1,
                    'fixtures': [
                        {
                            'density': 1,
                            'friction': 0,
                            'restitution': 0,
                            'shape': {
                                'type': 'rectangle'
                            },
                            'isSensor': False
                        }
                    ],
                    'jointType': 'weldJoint',
                    'unitAnchor': {
                        'x': 0,
                        'y': 33,
                        'rotation': 0
                    },
                    'itemAnchor': {
                        'x': 0,
                        'y': 0,
                        'lowerAngle': 0,
                        'upperAngle': 0
                    }
                }
            },
            'variables': {},
            'effects': {
                'attacked': {
                    'projectileType': '',
                    'sound': {},
                    'animation': '',
                    'tween': ''
                },
                'create': {
                    'projectileType': '',
                    'sound': {},
                    'animation': ''
                },
                'destroy': {
                    'projectileType': '',
                    'sound': {},
                    'animation': ''
                }
            },
            'confinedWithinMapBoundaries': True,
            'ai': {
                'pathFindingMethod': 'simple',
                'idleBehaviour': 'stay',
                'sensorResponse': 'none',
                'attackResponse': 'none',
                'maxTravelDistance': 300,
                'sensorRadius': 150,
                'maxAttackRange': 400
            },
            'defaultItems': [],
            'scripts': {
                'YnK58YN6ZD': {
                    'key': 'YnK58YN6ZD',
                    'folderName': 'abilities',
                    'parent': None,
                    'order': -1,
                    'expanded': True
                },
                'DOrbWp0AGz': {
                    'triggers': [],
                    'conditions': [
                        {
                            'operator': '==',
                            'operandType': 'boolean'
                        },
                        True,
                        True
                    ],
                    'actions': [
                        {
                            'type': 'stopUsingItem',
                            'entity': {
                                'function': 'getItemCurrentlyHeldByUnit',
                                'entity': {
                                    'function': 'thisEntity'
                                }
                            },
                            'hasFixedCSP': None,
                            'runOnClient': True
                        }
                    ],
                    'name': 'stop using item',
                    'parent': 'YnK58YN6ZD',
                    'key': 'DOrbWp0AGz',
                    'order': 1
                },
                'YFeMQ20gBX': {
                    'triggers': [],
                    'conditions': [
                        {
                            'operator': '==',
                            'operandType': 'boolean'
                        },
                        True,
                        True
                    ],
                    'actions': [
                        {
                            'type': 'startUsingItem',
                            'entity': {
                                'function': 'getItemCurrentlyHeldByUnit',
                                'entity': {
                                    'function': 'thisEntity'
                                }
                            },
                            'hasFixedCSP': None,
                            'runOnClient': True
                        }
                    ],
                    'name': 'start using item',
                    'parent': 'YnK58YN6ZD',
                    'key': 'YFeMQ20gBX',
                    'order': 0
                },
                'w2VrnZHyom': {
                    'triggers': [],
                    'conditions': [
                        {
                            'operator': '==',
                            'operandType': 'boolean'
                        },
                        True,
                        True
                    ],
                    'actions': [
                        {
                            'type': 'forAllEntities',
                            'entityGroup': {
                                'function': 'entitiesInRegion',
                                'region': {
                                    'function': 'entityBounds',
                                    'entity': {
                                        'function': 'thisEntity'
                                    }
                                }
                            },
                            'actions': [
                                {
                                    'type': 'condition',
                                    'conditions': [
                                        {
                                            'operandType': 'string',
                                            'operator': '=='
                                        },
                                        {
                                            'function': 'getEntityType',
                                            'entity': {
                                                'function': 'getSelectedEntity'
                                            }
                                        },
                                        'item'
                                    ],
                                    'then': [
                                        {
                                            'type': 'makeUnitPickupItem',
                                            'unit': {
                                                'function': 'thisEntity'
                                            },
                                            'item': {
                                                'function': 'getSelectedEntity'
                                            }
                                        }
                                    ],
                                    'else': []
                                }
                            ]
                        }
                    ],
                    'name': 'pick up item',
                    'parent': 'YnK58YN6ZD',
                    'key': 'w2VrnZHyom',
                    'order': 2
                },
                'yP67J1MMRN': {
                    'triggers': [],
                    'conditions': [
                        {
                            'operator': '==',
                            'operandType': 'boolean'
                        },
                        True,
                        True
                    ],
                    'actions': [
                        {
                            'type': 'dropItemAtPosition',
                            'item': {
                                'function': 'getItemCurrentlyHeldByUnit',
                                'entity': {
                                    'function': 'thisEntity'
                                }
                            },
                            'position': {
                                'function': 'getEntityPosition',
                                'entity': {
                                    'function': 'thisEntity'
                                }
                            }
                        }
                    ],
                    'name': 'drop item',
                    'parent': 'YnK58YN6ZD',
                    'key': 'yP67J1MMRN',
                    'order': 3
                }
            }
        }


class ItemTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'delayBeforeUse': 0,
            'bulletStartPosition': {
                'rotation': 0,
                'y': 0,
                'x': 0
            },
            'frames': {},
            'name': 'New Item Type',
            'handle': '',
            'attributes': {},
            'variables': {},
            'cellSheet': {
                'columnCount': 1,
                'rowCount': 1,
                'url': 'https://cache.modd.io/asset/spriteImage/1588259311826_Small Stick Tree Branch.png'
            },
            'inventoryImage': 'https://cache.modd.io/asset/spriteImage/1588879714036_test.png',
            'isStackable': False,
            'isPurchasable': True,
            'canBePurchasedBy': [],
            'isGun': False,
            'bulletDestroyedOnCollisionWithWall/unitType': 'raycast',
            'type': 'weapon',
            'hits': [],
            'states': {
                'selected': {
                    'name': 'selected',
                    'animation': 'default',
                    'body': 'selected',
                    'particles': {},
                    'sound': {}
                },
                'unselected': {
                    'name': 'unselected',
                    'animation': 'none',
                    'body': 'none',
                    'particles': {},
                    'sound': {}
                },
                'dropped': {
                    'name': 'dropped',
                    'animation': 'dropped',
                    'body': 'dropped',
                    'particles': {},
                    'sound': {}
                }
            },
            'animations': {
                'default': {
                    'framesPerSecond': 0,
                    'loopCount': 0,
                    'frames': [
                        1
                    ],
                    'name': 'default'
                }
            },
            'bodies': {
                'selected': {
                    'name': 'selected',
                    'type': 'spriteOnly',
                    'width': 12,
                    'height': 27,
                    'z-index': {
                        'layer': 3,
                        'depth': 4
                    },
                    'fixedRotation': False,
                    'constantSpeed +DestroyedOnCollisionWithWall/unit': False,
                    'allowSleep': True,
                    'collidesWith': {
                        'units': True,
                        'items': True,
                        'projectiles': True,
                        'walls': True,
                        'debris': False
                    },
                    'angularDamping': 1,
                    'linearDamping': 5,
                    'rotationSpeed': 3,
                    'spriteScale': 1,
                    'fixtures': [
                        {
                            'density': 1,
                            'friction': 0.01,
                            'restitution': 0.01,
                            'shape': {
                                'type': 'rectangle'
                            },
                            'isSensor': False
                        }
                    ],
                    'jointType': 'weldJoint',
                    'unitAnchor': {
                        'x': 0,
                        'y': 30
                    },
                    'itemAnchor': {
                        'x': 0,
                        'y': 58
                    }
                },
                'dropped': {
                    'name': 'dropped',
                    'type': 'dynamic',
                    'width': 12,
                    'height': 27,
                    'z-index': {
                        'layer': 1,
                        'depth': 2
                    },
                    'fixedRotation': False,
                    'constantSpeed +DestroyedOnCollisionWithWall/unit': False,
                    'allowSleep': True,
                    'collidesWith': {
                        'units': False,
                        'items': False,
                        'projectiles': False,
                        'walls': True,
                        'debris': False
                    },
                    'angularDamping': 1,
                    'linearDamping': 1,
                    'rotationSpeed': 1,
                    'spriteScale': 1,
                    'fixtures': [
                        {
                            'density': 1,
                            'friction': 0,
                            'restitution': 0,
                            'shape': {
                                'type': 'rectangle'
                            },
                            'isSensor': False
                        }
                    ],
                    'jointType': 'weldJoint',
                    'unitAnchor': {
                        'x': 0,
                        'y': 48
                    },
                    'itemAnchor': {
                        'x': 0,
                        'y': 58
                    },
                    'bullet': False
                }
            },
            'hideIfUnaffordable': False,
            'projectileType': '',
            'quantity': None,
            'maxQuantity': None,
            'description': None,
            'reloadRate': 2800,
            'recoilForce': 0,
            'fireRate': 500,
            'bulletDestroyedOnCollisionWithWall/unitForce': 14,
            'knockbackForce': 0,
            'effects': {
                'reload': {
                    'animation': '',
                    'sound': {}
                },
                'empty': {
                    'animation': '',
                    'sound': {}
                },
                'destroy': {
                    'runScript': '',
                    'animation': '',
                    'sound': {},
                    'projectileType': ''
                },
                'create': {
                    'runScript': '',
                    'animation': '',
                    'sound': {},
                    'projectileType': ''
                },
                'use': {
                    'runScript': '',
                    'tween': 'none',
                    'animation': 'use',
                    'sound': {},
                    'projectileType': ''
                }
            },
            'bulletDestroyedOnCollisionWithWall/unitStartPosition': {
                'x': 0,
                'y': 0,
                'rotation': 0
            },
            'bulletDestroyedOnCollisionWithWall/unitDistance': 1300,
            'penetration': False,
            'destroyTimer': 30000,
            'particles': {},
            'damage': {
                'unitAttributes': {
                    'health': 10
                }
            },
            'sound': {},
            'canBeUsedBy': [],
            'isUsedOnPickup': False,
            'removeWhenEmpty': False,
            'bonus': {
                'consume': {
                    'playerAttribute': {},
                    'unitAttribute': {}
                },
                'passive': {
                    'playerAttribute': {},
                    'unitAttribute': {}
                }
            },
            'cost': {
                'quantity': 0
            },
            'buffTypes': [],
            'carriedBy': [],
            'controls': {
                'undroppable': False,
                'permittedInventorySlots': [],
                'mouseBehaviour': {
                    'rotateToFaceMouseCursor': True,
                    'flipSpriteHorizontallyWRTMouse': False
                }
            },
            'damageHitBox': {
                'width': 60,
                'height': 30,
                'offsetX': 0,
                'offsetY': 50
            },
            'damageDelay': 0,
            'projectileStreamMode': '0',
            'lifeSpan': None,
            'ignoreServerStream': False,
            'confinedWithinMapBoundaries': True,
            'scripts': {}
        }


class ProjectileTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'inventoryImage': '',
            'name': 'New Projectile Type',
            'attributes': {},
            'variables': {},
            'states': {
                'zTzPFYOZkc': {
                    'name': 'default',
                    'sound': {},
                    'particles': {},
                    'animation': 'default',
                    'body': 'default'
                }
            },
            'animations': {
                'default': {
                    'framesPerSecond': 0,
                    'loopCount': 0,
                    'frames': [
                        1
                    ],
                    'name': 'default'
                }
            },
            'bodies': {
                'default': {
                    'bullet': True,
                    'name': 'default',
                    'type': 'dynamic',
                    'width': 10,
                    'height': 32,
                    'z-index': {
                        'layer': 3,
                        'depth': 1
                    },
                    'fixedRotation': False,
                    'constantSpeed +DestroyedOnCollisionWithWall/unit': True,
                    'allowSleep': False,
                    'collidesWith': {
                        'units': True,
                        'items': True,
                        'projectiles': False,
                        'walls': True,
                        'debris': False
                    },
                    'angularDamping': 1,
                    'linearDamping': 0,
                    'rotationSpeed': 1,
                    'spriteScale': 1,
                    'fixtures': [
                        {
                            'density': 1,
                            'friction': 0.01,
                            'restitution': 0.01,
                            'shape': {
                                'type': 'rectangle'
                            },
                            'isSensor': True
                        }
                    ],
                    'jointType': 'weldJoint',
                    'unitAnchor': {
                        'x': 0,
                        'y': 33,
                        'rotation': 0
                    },
                    'itemAnchor': {
                        'x': 0,
                        'y': 0,
                        'lowerAngle': 0,
                        'upperAngle': 0
                    }
                }
            },
            'destroyTimer': 1500,
            'cellSheet': {
                'url': 'https://cache.modd.io/asset/spriteImage/1588265261495_Long Yellow Bullet.png',
                'rowCount': 1,
                'columnCount': 1
            },
            'lifeSpan': 1500,
            'effects': {
                'create': {
                    'projectileType': '',
                    'sound': {},
                    'animation': '',
                    'runScript': ''
                },
                'destroy': {
                    'projectileType': '',
                    'sound': {},
                    'animation': '',
                    'runScript': ''
                }
            },
            'destroyOnContactWith': {
                'units': True,
                'items': True,
                'projectiles': True,
                'walls': True,
                'debris': True
            }
        }


class PlayerTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'name': 'New Player Type',
            'attributes': {},
            'color': 'white',
            'relationships': {},
            'showNameLabel': True
        }


class AttributeTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'color': 'white',
            'dataType': '',
            'decimalPlaces': 0,
            'displayValue': False,
            'isVisible': False,
            'max': 100,
            'min': 0,
            'name': 'New Attribute Type',
            'regenerateSpeed': 0,
            'showAsHUD': True,
            'showWhen': '',
            'value': 0
        }


class AnimationTypeBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'frames': [
                1
            ],
            'framesPerSecond': 0,
            'loopCount': 0,
            'name': 'New Animation Type'
        }


class StateBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'animation': 'default',
            'body': 'default',
            'name': 'New State',
            'particles': {},
            'sound': {}
        }


class ShopBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'dismissible': True,
            'itemTypes': {},
            'name': 'New Shop',
            'unitTypes': {}
        }


class MusicBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'file': '',
            'name': 'New Song',
            'volume': 25
        }


class SoundBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'name': 'New Sound',
            'file': '',
            'volume': 100
        }


class DialogueBase(VariableType):
    def __init__(self, id=None, name=None):
        super().__init__(id, name=name)

    def get_template_data(self):
        return {
            'name': 'New Dialogue',
            'dialogueTitle': 'New Dialogue',
            'message': '',
            'image': '',
            'letterPrintSpeed': 20,
            'options': []
        }
