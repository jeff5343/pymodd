from pymodd.functions import Variable, Shop, AnimationType, State, ItemType, Music, UnitType, AttributeType, PlayerType


class EntityTypeVariables():
    TARGET_UNIT = Variable('targetUnit')
    SENSOR_RADIUS = Variable('sensorRadius')


class Shops():
    FROGE_SHOP = Shop('OJbEQyc7is')


class AnimationTypes():
    DROPPED = AnimationType('dropped')
    DEFAULT = AnimationType('default')
    USE = AnimationType('use')
    TONGUE_OUT = AnimationType('B1cWOYKvNL')


class States():
    UNSELECTED = State('unselected')
    DEFAULT = State('default')
    SELECTED = State('selected')
    DROPPED = State('dropped')
    TONGUE_OUT = State('r60qiEIvyt')


class ProjectileTypes():
    pass


class ItemTypes():
    KNIFE = ItemType('bMDJQyFACm')
    FROG_TONGUE = ItemType('BBCDO38dr7')
    FROG_SWORD = ItemType('tmAlzggQX4')
    BOSS_FROG_TONGUE = ItemType('AqrGZUYBdS')


class Musics():
    D = Music('iJ8RoRfyeu')


class Sounds():
    pass


class UnitTypes():
    POOPER = UnitType('fighter')
    FROG = UnitType('oTDQ3jlcMa')
    FROG_BOSS = UnitType('TyaKyQzgKc')


class Variables():
    AI = Variable('AI')
    TEMP_UNIT = Variable('tempUnit')
    BOSS_TIMER = Variable('bossTimer')
    I = Variable('i')
    TIMER = Variable('timer')


class AttributeTypes():
    SPEED = AttributeType('speed')
    HEALTH = AttributeType('health')
    MOVE = AttributeType('G3adwzJecn')
    FROG_KILLS = AttributeType('yjdyHZbWpA')


class PlayerTypes():
    PLAYER = PlayerType('humanPlayer')
    AI = PlayerType('eA9ZwoweVz')


class PlayerTypeVariables():
    pass
