from pymodd.variable_types import AnimationType, AttributeType, Dialogue, EntityVariable, ItemType, Music, PlayerType, PlayerVariable, ProjectileType, Shop, Sound, State, UnitType, Variable, DataType


class ItemTypes:
    BOSS_FROG_TONGUE = ItemType('AqrGZUYBdS', name='Boss Frog Tongue')
    FROG_TONGUE = ItemType('BBCDO38dr7', name='Frog Tongue')
    KNIFE = ItemType('bMDJQyFACm', name='Knife')
    FROG_SWORD = ItemType('tmAlzggQX4', name='Frog Sword')


class ProjectileTypes:
    pass


class UnitTypes:
    FROG_BOSS = UnitType('TyaKyQzgKc', name='Frog Boss')
    POOPER = UnitType('fighter', name='Pooper')
    FROG = UnitType('oTDQ3jlcMa', name='Frog')


class PlayerTypes:
    AI = PlayerType('eA9ZwoweVz', name='ai')
    PLAYER = PlayerType('humanPlayer', name='Player')


class ItemTypeGroups:
    RANDOMGROUP = Variable('randomgroup', DataType.ITEM_TYPE_GROUP, default_value=[ItemTypes.FROG_TONGUE, ItemTypes.KNIFE, ItemTypes.FROG_SWORD])


class UnitTypeGroups:
    UNITTYPEGROUP = Variable('unittypegroup', DataType.UNIT_TYPE_GROUP, default_value=[UnitTypes.FROG_BOSS, UnitTypes.POOPER, UnitTypes.FROG])


class Variables:
    AI = Variable('AI', DataType.PLAYER, default_value='computer1')
    BOSS_TIMER = Variable('bossTimer', DataType.NUMBER, default_value=0)
    DWADAWD = Variable('dwadawd', DataType.UNIT_GROUP)
    TEMP_UNIT = Variable('tempUnit', DataType.UNIT)
    TIMER = Variable('timer', DataType.NUMBER, default_value=0)


class EntityVariables:
    SENSOR_RADIUS = EntityVariable('sensorRadius', DataType.NUMBER)
    TARGET_UNIT = EntityVariable('targetUnit', DataType.UNIT)


class PlayerVariables:
    TARGET_UNIT = PlayerVariable('targetUnit', DataType.UNIT)


class Regions:
    pass


class Shops:
    FROGE_SHOP = Shop('OJbEQyc7is', name='Froge Shop')


class Dialogues:
    pass


class Musics:
    D = Music('iJ8RoRfyeu', name='d')


class Sounds:
    pass


class States:
    DEFAULT = State('default', name='default')
    DROPPED = State('dropped', name='dropped')
    TONGUE_OUT = State('r60qiEIvyt', name='tongue out')
    SELECTED = State('selected', name='selected')
    UNSELECTED = State('unselected', name='unselected')


class AnimationTypes:
    TONGUE_OUT = AnimationType('B1cWOYKvNL', name='tongue out')
    DEFAULT = AnimationType('default', name='default')
    DROPPED = AnimationType('dropped', name='dropped')
    USE = AnimationType('use', name='use')


class AttributeTypes:
    MOVE = AttributeType('G3adwzJecn', name='move')
    HEALTH = AttributeType('health', name='health ')
    SPEED = AttributeType('speed', name='speed')
    FROG_KILLS = AttributeType('yjdyHZbWpA', name='frog kills')


