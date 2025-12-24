from pymodd.variable_types import AnimationTypeBase, AttributeTypeBase, DialogueBase, EntityVariableBase, ItemTypeBase, MusicBase, PlayerTypeBase, PlayerVariableBase, ProjectileTypeBase, ShopBase, SoundBase, StateBase, UnitTypeBase, VariableBase
from pymodd.variable.data_type import DataType


class ItemType:
    BOSS_FROG_TONGUE = ItemTypeBase('AqrGZUYBdS', name='Boss Frog Tongue')
    FROG_TONGUE = ItemTypeBase('BBCDO38dr7', name='Frog Tongue')
    KNIFE = ItemTypeBase('bMDJQyFACm', name='Knife')
    FROG_SWORD = ItemTypeBase('tmAlzggQX4', name='Frog Sword')


class ProjectileType:
    pass


class UnitType:
    FROG_BOSS = UnitTypeBase('TyaKyQzgKc', name='Frog Boss')
    USER = UnitTypeBase('fighter', name='User')
    FROG = UnitTypeBase('oTDQ3jlcMa', name='Frog')


class PlayerType:
    AI = PlayerTypeBase('eA9ZwoweVz', name='ai')
    PLAYER = PlayerTypeBase('humanPlayer', name='Player')


class ItemTypeGroup:
    RANDOMGROUP = VariableBase('randomgroup', DataType.ITEM_TYPE_GROUP, default_value=[ItemType.FROG_TONGUE, ItemType.KNIFE, ItemType.FROG_SWORD])


class UnitTypeGroup:
    UNITTYPEGROUP = VariableBase('unittypegroup', DataType.UNIT_TYPE_GROUP, default_value=[UnitType.FROG_BOSS, UnitType.USER, UnitType.FROG])


class Variable:
    AI = VariableBase('AI', DataType.PLAYER, default_value='computer1')
    BOSS_TIMER = VariableBase('bossTimer', DataType.NUMBER, default_value=0)
    DWADAWD = VariableBase('dwadawd', DataType.UNIT_GROUP)
    TEMP_UNIT = VariableBase('tempUnit', DataType.UNIT)
    TIMER = VariableBase('timer', DataType.NUMBER, default_value=0)


class EntityVariable:
    SENSOR_RADIUS = EntityVariableBase('sensorRadius', DataType.NUMBER)
    TARGET_UNIT = EntityVariableBase('targetUnit', DataType.UNIT)


class PlayerVariable:
    TARGET_UNIT = PlayerVariableBase('targetUnit', DataType.UNIT)


class Region:
    pass


class Shop:
    FROGE_SHOP = ShopBase('OJbEQyc7is', name='Froge Shop')


class Dialogue:
    pass


class Music:
    D = MusicBase('iJ8RoRfyeu', name='d')


class Sound:
    pass


class State:
    DEFAULT = StateBase('default', name='default')
    DROPPED = StateBase('dropped', name='dropped')
    TONGUE_OUT = StateBase('r60qiEIvyt', name='tongue out')
    SELECTED = StateBase('selected', name='selected')
    UNSELECTED = StateBase('unselected', name='unselected')


class AnimationType:
    TONGUE_OUT = AnimationTypeBase('B1cWOYKvNL', name='tongue out')
    DEFAULT = AnimationTypeBase('default', name='default')
    DROPPED = AnimationTypeBase('dropped', name='dropped')
    USE = AnimationTypeBase('use', name='use')


class AttributeType:
    MOVE = AttributeTypeBase('G3adwzJecn', name='move')
    HEALTH = AttributeTypeBase('health', name='health ')
    SPEED = AttributeTypeBase('speed', name='speed')
    FROG_KILLS = AttributeTypeBase('yjdyHZbWpA', name='frog kills')


