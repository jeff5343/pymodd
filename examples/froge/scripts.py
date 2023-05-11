from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Trigger, UiTarget, Flip, script

from game_variables import *


@script(triggers=[Trigger.GAME_START])
class Initialize():
	def _build(self):
		assign_player_to_player_type(Variables.AI, PlayerTypes.AI)


@script(triggers=[Trigger.PLAYER_JOINS_GAME])
class PlayerJoins():
	def _build(self):
		create_unit_for_player_at_position_with_rotation(UnitTypes.POOPER, LastTriggeringPlayer(), RandomPositionInRegion(EntireMapRegion()), 0)
		make_camera_of_player_track_unit(LastTriggeringPlayer(), LastCreatedUnit())
		assign_player_to_player_type(LastTriggeringPlayer(), PlayerTypes.PLAYER)


@script(triggers=[Trigger.PLAYER_LEAVES_GAME])
class PlayerLeaves():
	def _build(self):
		for unit in AllUnitsOwnedByPlayer(LastTriggeringPlayer()):
			destroy_entity(unit)


@script(triggers=[Trigger.EVERY_SECOND])
class EverySecond():
	def _build(self):
		if NumberOfUnitsOfUnitType(UnitTypes.FROG) < 5:
			create_unit_for_player_at_position_with_rotation(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0)
		else:
			if NumberOfUnitsOfUnitType(UnitTypes.FROG_BOSS) == 0:
				if Variables.BOSS_TIMER <= 0:
					create_unit_for_player_at_position_with_rotation(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0)
					update_ui_target_for_player_for_miliseconds(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000)
				decrease_variable_by_number(Variables.BOSS_TIMER, 1)


@script(triggers=[Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO])
class WhenAUnitsAttributeBecomes0OrLess():
	def _build(self):
		if AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeTypes.HEALTH:
			if PlayerTypeOfPlayer(OwnerOfEntity(LastTriggeringUnit())) == PlayerTypes.PLAYER:
				set_entity_attribute(AttributeTypes.HEALTH, LastTriggeringUnit(), AttributeMaxOfEntity(AttributeTypes.HEALTH, LastTriggeringUnit()))
				set_entity_variable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit(), Undefined())
				move_entity_to_position(LastTriggeringUnit(), CenterOfRegion(EntireMapRegion()))
			else:
				if UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS:
					set_variable(Variables.BOSS_TIMER, 200)
					set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), ValueOfPlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 7)
				else:
					set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), ValueOfPlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 1)
				destroy_entity(LastTriggeringUnit())
		else:
			if AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeTypes.MOVE:
				set_entity_variable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit(), Undefined())
				for entity in AllEntitiesInRegion(DynamicRegion(XCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), YCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()))):
					if PlayerTypeOfPlayer(OwnerOfEntity(entity)) == PlayerTypes.PLAYER:
						if ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit()) == Undefined() or DistanceBetweenPositions(PositionOfEntity(entity), PositionOfEntity(LastTriggeringUnit())) > DistanceBetweenPositions(PositionOfEntity(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit())), PositionOfEntity(LastTriggeringUnit())):
							create_floating_text_at_position_with_color('Froge sense', PositionOfEntity(LastTriggeringUnit()), '#327117', disabled=True)
							set_entity_variable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit(), entity)
				if ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit()) != Undefined():
					rotate_entity_instantly_to_face_position(LastTriggeringUnit(), PositionOfEntity(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit())))
					if UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS:
						apply_force_on_entity_at_angle(RandomNumberBetween(3000, 6000), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
					else:
						apply_force_on_entity_at_angle(RandomNumberBetween(300, 600), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
					use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(LastTriggeringUnit()))
				else:
					rotate_entity_instantly_to_face_position(LastTriggeringUnit(), RandomPositionInRegion(EntityBounds(LastTriggeringUnit())))
					if UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS:
						apply_force_on_entity_at_angle(RandomNumberBetween(1500, 3500), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
					else:
						apply_force_on_entity_at_angle(RandomNumberBetween(150, 400), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
					stop_using_item(ItemCurrentlyHeldByUnit(LastTriggeringUnit()))
				set_entity_attribute(AttributeTypes.MOVE, LastTriggeringUnit(), RandomNumberBetween(35, 100))


@script(triggers=[])
class OpenShop():
	def _build(self):
		open_shop_for_player(Shops.FROGE_SHOP, OwnerOfEntity(LastCastingUnit()))

