from pymodd.functions import UnitType, PlayerType, ItemType, Variable, EntityVariable, AnimationType, AttributeType, State, Shop, Music


class UnitTypes:
	FROG_BOSS = UnitType("TyaKyQzgKc")
	POOPER = UnitType("fighter")
	FROG = UnitType("oTDQ3jlcMa")


class PlayerTypes:
	AI = PlayerType("eA9ZwoweVz")
	PLAYER = PlayerType("humanPlayer")


class ItemTypes:
	BOSS_FROG_TONGUE = ItemType("AqrGZUYBdS")
	FROG_TONGUE = ItemType("BBCDO38dr7")
	KNIFE = ItemType("bMDJQyFACm")
	FROG_SWORD = ItemType("tmAlzggQX4")


class ProjectileTypes:
	pass


class Regions:
	pass


class Variables:
	AI = Variable("AI", variable_type='player')
	BOSS_TIMER = Variable("bossTimer", variable_type='number')
	DWADAWD = Variable("dwadawd", variable_type='unitGroup')
	TEMP_UNIT = Variable("tempUnit", variable_type='unit')
	TIMER = Variable("timer", variable_type='number')


class EntityVariables:
	SENSOR_RADIUS = EntityVariable("sensorRadius", variable_type='number')
	TARGET_UNIT = EntityVariable("targetUnit", variable_type='unit')


class PlayerVariables:
	pass


class AnimationTypes:
	TONGUE_OUT = AnimationType("B1cWOYKvNL")
	DEFAULT = AnimationType("default")
	DROPPED = AnimationType("dropped")
	USE = AnimationType("use")


class AttributeTypes:
	MOVE = AttributeType("G3adwzJecn")
	HEALTH = AttributeType("health")
	SPEED = AttributeType("speed")
	FROG_KILLS = AttributeType("yjdyHZbWpA")


class ItemTypeGroups:
	RANDOMGROUP = Variable("randomgroup", variable_type='itemTypeGroup')


class UnitTypeGroups:
	UNITTYPEGROUP = Variable("unittypegroup", variable_type='unitTypeGroup')


class States:
	DEFAULT = State("default")
	DROPPED = State("dropped")
	TONGUE_OUT = State("r60qiEIvyt")
	SELECTED = State("selected")
	UNSELECTED = State("unselected")


class Shops:
	FROGE_SHOP = Shop("OJbEQyc7is")


class Dialogues:
	pass


class Musics:
	D = Music("iJ8RoRfyeu")


class Sounds:
	pass


