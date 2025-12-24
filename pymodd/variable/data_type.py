from enum import Enum


class DataType(Enum):
    NUMBER = "number"
    STRING = "string"
    BOOLEAN = "boolean"
    ITEM = "item"
    UNIT = "unit"
    PLAYER = "player"
    PROJECTILE = "projectile"
    ITEM_TYPE = "itemType"
    UNIT_TYPE = "unitType"
    PLAYER_TYPE = "playerType"
    PROJECTILE_TYPE = "projectileType"
    ITEM_GROUP = "itemGroup"
    UNIT_GROUP = "unitGroup"
    PLAYER_GROUP = "playerGroup"
    ITEM_TYPE_GROUP = "itemTypeGroup"
    UNIT_TYPE_GROUP = "unitTypeGroup"
    REGION = "region"
    PARTICLE_TYPE = "particleType"
