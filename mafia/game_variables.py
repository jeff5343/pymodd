from pymodd.functions import UnitType, PlayerType, ItemType, Variable, EntityVariable, PlayerVariable, AnimationType, AttributeType, State, Shop, Dialogue


class UnitTypes:
	TREE = UnitType("4okhUTCTbS")
	COOKIE = UnitType("8cyriU2Wzn")
	MAYOR = UnitType("DOV1Qo2gN7")
	DEAD = UnitType("EgbtKm58QY")
	MAP = UnitType("Jj7xVVvC9b")
	KNIFE = UnitType("RKicYG2t0F")
	NIGHT = UnitType("RoavKZRhuZ")
	CITIZEN = UnitType("jxRTvmHjpH")
	BOUNDARY = UnitType("xMilVT7dWd")
	LOBBY_UNIT = UnitType("xvZMmubV1a")
	GRAVESTONE = UnitType("zQykbdtsGL")
	HANGER = UnitType("zYcKjaniSO")


class PlayerTypes:
	AI = PlayerType("1BWIMbOoMx")
	AI_SHOW_S_NAME = PlayerType("VxbQ51emtN")
	NEUTRAL = PlayerType("W7GqeSnVms")
	VILLAGERS = PlayerType("humanPlayer")
	MAFIA = PlayerType("oyB9iELCEY")
	DEAD = PlayerType("wylTa12rPd")


class ItemTypes:
	HAPPY = ItemType("2hwnjZwDjD")
	LAZY = ItemType("M9akZB4QIL")
	WHALE = ItemType("YVGrb9Fx08")
	CRYING = ItemType("aKFAkNIjNP")
	CUTE = ItemType("h3x4o5rMBn")
	SCARED = ItemType("iFFPzSSJT7")
	ANGRY = ItemType("kMpYQDMwB6")


class ProjectileTypes:
	pass


class Regions:
	BOUNDARY1 = Variable("boundary1", variable_type='region')
	BOUNDARY2 = Variable("boundary2", variable_type='region')
	BOUNDARY3 = Variable("boundary3", variable_type='region')
	BOUNDARY4 = Variable("boundary4", variable_type='region')
	GRAVEYARD = Variable("graveyard", variable_type='region')
	LYNCH_ZONE = Variable("lynchZone", variable_type='region')
	MUD1 = Variable("mud1", variable_type='region')
	MUD2 = Variable("mud2", variable_type='region')
	SPAWN = Variable("spawn", variable_type='region')
	WATER1 = Variable("water1", variable_type='region')
	WATER2 = Variable("water2", variable_type='region')


class Variables:
	AI = Variable("ai", variable_type='player')
	AVAILABLE_ROLES = Variable("availableRoles", variable_type='string')
	BREAK = Variable("break", variable_type='string')
	C_MESSAGE = Variable("cMessage", variable_type='string')
	CHANGE_UNIT = Variable("changeUnit", variable_type='unit')
	CHAOS_ROLES = Variable("chaosRoles", variable_type='string')
	COOKIE_TARGET = Variable("cookieTarget", variable_type='player')
	CULT_MEMBERS = Variable("cultMembers", variable_type='string')
	CULTIST = Variable("cultist", variable_type='player')
	DIALOGUE_MESSAGE = Variable("dialogueMessage", variable_type='string')
	DIALOGUE_MESSAGE2 = Variable("dialogueMessage2", variable_type='string')
	DIALOGUE_MESSAGE3 = Variable("dialogueMessage3", variable_type='string')
	DIALOGUE_TITLE = Variable("dialogueTitle", variable_type='string')
	DID_MAYOR_REVAL = Variable("didMayorReval", variable_type='boolean')
	DID_VIGILANTE_SCREW_UP = Variable("didVigilanteScrewUp", variable_type='boolean')
	E_MESSAGE = Variable("eMessage", variable_type='string')
	EXECUTIONER = Variable("executioner", variable_type='player')
	EXECUTIONER_TARGET = Variable("executionerTarget", variable_type='player')
	FINAL_LYNCH_VOTE = Variable("finalLynchVote", variable_type='number')
	FRAMED_PLAYER = Variable("framedPlayer", variable_type='player')
	G = Variable("g", variable_type='number')
	GAMEMODE = Variable("gamemode", variable_type='string')
	GAMEMODE_ROLES = Variable("gamemodeRoles", variable_type='string')
	GAMEMODE_VOTES = Variable("gamemodeVotes", variable_type='string')
	GODFATHER = Variable("godfather", variable_type='player')
	GODFATHER_IS_PRESENT = Variable("godfatherIsPresent", variable_type='boolean')
	GRAVEYARD_MANAGER = Variable("graveyardManager", variable_type='player')
	HEALED_PLAYER = Variable("healedPlayer", variable_type='player')
	I = Variable("i", variable_type='number')
	INVESTIGATED_PLAYER = Variable("investigatedPlayer", variable_type='player')
	J = Variable("j", variable_type='number')
	KILLING_PLAYER = Variable("killingPlayer", variable_type='player')
	LYNCH_VOTES = Variable("lynchVotes", variable_type='string')
	LYNCHED_ROLE = Variable("lynchedRole", variable_type='string')
	LYNCHING_PLAYER = Variable("lynchingPlayer", variable_type='player')
	MAFIA_PLAYERS = Variable("mafiaPlayers", variable_type='string')
	MAFIA_VOTES = Variable("mafiaVotes", variable_type='string')
	MODS = Variable("mods", variable_type='string')
	NAMES = Variable("names", variable_type='string')
	NEUTRAL_PLAYERS = Variable("neutralPlayers", variable_type='string')
	NIGHT_NUMBER = Variable("nightNumber", variable_type='number')
	NIGHT_UNIT = Variable("nightUnit", variable_type='unit')
	NO_KILLING_NIGHTS = Variable("noKillingNights", variable_type='number')
	OTHER_ROLES = Variable("otherRoles", variable_type='string')
	PLAYERS_ABSTAINED = Variable("playersAbstained", variable_type='number')
	PLAYERS_NEEDED_TO_READY_UP = Variable("playersNeededToReadyUp", variable_type='number')
	PLAYERS_READIED_UP = Variable("playersReadiedUp", variable_type='number')
	PLAYERS_VOTED = Variable("playersVoted", variable_type='number')
	RANDOM_NEUTRAL_ROLES = Variable("randomNeutralRoles", variable_type='string')
	SPAN_END = Variable("span end", variable_type='string')
	SPAN_GREEN = Variable("span green", variable_type='string')
	SPAN_GREY = Variable("span grey", variable_type='string')
	SPAN_RED = Variable("span red", variable_type='string')
	STATE = Variable("state", variable_type='string')
	TEMP_BOOLEAN = Variable("tempBoolean", variable_type='boolean')
	TEMP_PLAYER = Variable("tempPlayer", variable_type='player')
	TEMP_STRING = Variable("tempString", variable_type='string')
	TEMP_UNIT = Variable("tempUnit", variable_type='unit')
	TIMER = Variable("timer", variable_type='number')
	TO_DIE = Variable("toDie", variable_type='string')
	TRIAL_MODS = Variable("trialMods", variable_type='string')
	UNBAN_WAITING_LIST = Variable("unbanWaitingList", variable_type='string')
	VIGILANTE_ARROWS = Variable("vigilanteArrows", variable_type='number')
	VILLAGER_PLAYERS = Variable("villagerPlayers", variable_type='string')
	WATCHER_TARGET = Variable("watcherTarget", variable_type='player')
	WATCHER_TARGET_VISITORS = Variable("watcherTargetVisitors", variable_type='string')
	WAYS_TO_DIE = Variable("waysToDie", variable_type='string')


class EntityVariables:
	ROLE = EntityVariable("role", variable_type='string')
	SKIN_NUMBER = EntityVariable("skinNumber", variable_type='number')
	TARGET_UNIT = EntityVariable("targetUnit", variable_type='unit')


class PlayerVariables:
	CURRENTLY_INPUTTING = PlayerVariable("currentlyInputting", variable_type='string')
	DID_VOTE = PlayerVariable("didVote", variable_type='boolean')
	ROLE = PlayerVariable("role", variable_type='string')
	SKIN_NUMBER = PlayerVariable("skinNumber", variable_type='number')
	UNBAN_TIME = PlayerVariable("unbanTime", variable_type='number')
	VOTES = PlayerVariable("votes", variable_type='number')


class AnimationTypes:
	HAPPY = AnimationType("0PaI5Uk9oj")
	CRYING = AnimationType("5aO95vZDL7")
	NO_FLOWER = AnimationType("81cNeGz45W")
	ANGRY = AnimationType("BhghzXsYov")
	WHALE = AnimationType("GXyWxCPzVp")
	SCARED = AnimationType("VytTF2N1m4")
	LAZY = AnimationType("WpcQOsBkSu")
	TO_DAY = AnimationType("Yjo3YT7hkY")
	DEFAULT = AnimationType("default")
	DROPPED = AnimationType("dropped")
	CUTE = AnimationType("hntSP6OBNK")
	FLOWER = AnimationType("tK1OgNPSmW")
	ANIMATION = AnimationType("use")
	TO_NIGHT = AnimationType("y6s7DBMqUg")


class AttributeTypes:
	DEAD_CHAT_COOLDOWN = AttributeType("KY6UPJamIQ")
	WINS = AttributeType("LdyOznb1fk")
	READY = AttributeType("XMCvG8aTmG")
	HEALTH = AttributeType("health")
	AFK_TIMER = AttributeType("qGog9hsljV")
	SPEED = AttributeType("speed")


class ItemTypeGroups:
	pass


class UnitTypeGroups:
	pass


class States:
	DAY = State("03hImugcPx")
	ANGRY = State("6aysAWIU4o")
	NIGHT = State("AdUsgzANVB")
	FLOWER = State("LRDCEf2Tae")
	LAZY = State("NuF8FBrKTX")
	DEFAULT = State("default")
	DROPPED = State("dropped")
	WHALE = State("lcan3m9eWW")
	HAPPY = State("lyioBVN2Jv")
	SCARED = State("n7wdqBR1q7")
	CRYING = State("nUayC09rlg")
	CUTE = State("njbU4buGP1")
	NO_FLOWER = State("rE1G4H7dh3")
	SELECTED = State("selected")
	UNSELECTED = State("unselected")


class Shops:
	SKIN_SHOP = Shop("hWn8hsQhRJ")


class Dialogues:
	ROLE_DESCRIPTOR = Dialogue("4b2j3uXScL")
	ABILITY_RESULT = Dialogue("DjmpBa07ff")
	HELP_BOREDOM = Dialogue("M5lpulKHgU")
	MODE_SELECTION = Dialogue("SAW8pc3Bwe")
	MAYOR_REVEAL_CHOICE = Dialogue("XB1aLkHLDA")
	ROUND_OVER = Dialogue("ZZvB8YGXmH")
	GAME_INFO = Dialogue("abH7epkh8s")
	FIRST_NIGHT_DEATH = Dialogue("dwhymJYXpN")
	FINAL_VOTE = Dialogue("kwnFeKStOt")
	GAME_INFO_PT_2 = Dialogue("yGkY8830bj")


class Musics:
	pass


class Sounds:
	pass


