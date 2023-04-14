from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Trigger, UiTarget, Flip, script

from game_variables import *


@script(triggers=[Trigger.GAME_START])
class Initialize():
	def _build(self):
		self.actions = [
			assign_player_to_player_type(Variables.AI, PlayerTypes.AI),
			
		]


@script(triggers=[Trigger.PLAYER_JOINS_GAME])
class PlayerJoins():
	def _build(self):
		self.actions = [
			create_unit_for_player_at_position_with_rotation(UnitTypes.POOPER, LastTriggeringPlayer(), RandomPositionInRegion(EntireMapRegion()), 0),
			make_camera_of_player_track_unit(LastTriggeringPlayer(), LastCreatedUnit()),
			assign_player_to_player_type(LastTriggeringPlayer(), PlayerTypes.PLAYER),
			
		]


@script(triggers=[Trigger.PLAYER_LEAVES_GAME])
class PlayerLeaves():
	def _build(self):
		self.actions = [
			for_all_units_in(AllUnitsOwnedByPlayer(LastTriggeringPlayer()), [
				destroy_entity(SelectedUnit()),
				
			], comment='when a player leaves, destroy all units owned by that player'),
			
		]


@script(triggers=[Trigger.EVERY_SECOND])
class EverySecond():
	def _build(self):
		self.actions = [
			if_else((NumberOfUnitsOfUnitType(UnitTypes.FROG) < 5), [
				create_unit_for_player_at_position_with_rotation(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
				
			], [
				if_else((NumberOfUnitsOfUnitType(UnitTypes.FROG_BOSS) == 0), [
					if_else((Variables.BOSS_TIMER <= 0), [
						create_unit_for_player_at_position_with_rotation(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
						update_ui_target_for_player_for_miliseconds(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000),
						set_variable(Variables.BOSS_TIMER, 200),
						
					], [
						
					]),
					decrease_variable_by_number(Variables.BOSS_TIMER, 1),
					
				], [
					
				]),
				
			]),
			
		]


@script(triggers=[Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO])
class WhenAUnitsAttributeBecomes0OrLess():
	def _build(self):
		self.actions = [
			if_else((AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeTypes.HEALTH), [
				if_else((PlayerTypeOfPlayer(OwnerOfEntity(LastTriggeringUnit())) == PlayerTypes.PLAYER), [
					set_entity_attribute(AttributeTypes.HEALTH, LastTriggeringUnit(), AttributeMaxOfEntity(AttributeTypes.HEALTH, LastTriggeringUnit())),
					set_entity_variable(EntityVariables.TARGET_UNIT, LastTriggeringUnit(), Undefined()),
					move_entity_to_position(LastTriggeringUnit(), CenterOfRegion(EntireMapRegion())),
					
				], [
					if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
						set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 7),
						
					], [
						set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 1),
						
					]),
					destroy_entity(LastTriggeringUnit()),
					
				]),
				
			], [
				if_else((AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeTypes.MOVE), [
					set_entity_variable(EntityVariables.TARGET_UNIT, LastTriggeringUnit(), Undefined()),
					for_all_entities_in(AllEntitiesInRegion(DynamicRegion(XCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), YCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()))), [
						if_else((PlayerTypeOfPlayer(OwnerOfEntity(SelectedEntity())) == PlayerTypes.PLAYER), [
							if_else(((ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()) == Undefined()) | (DistanceBetweenPositions(PositionOfEntity(SelectedEntity()), PositionOfEntity(LastTriggeringUnit())) > DistanceBetweenPositions(PositionOfEntity(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit())), PositionOfEntity(LastTriggeringUnit())))), [
								create_floating_text_at_position_with_color('Froge sense', PositionOfEntity(LastTriggeringUnit()), '#327117', disabled=True),
								set_entity_variable(EntityVariables.TARGET_UNIT, LastTriggeringUnit(), SelectedEntity()),
								
							], [
								
							]),
							
						], [
							
						]),
						
					]),
					if_else((ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()) != Undefined()), [
						rotate_entity_instantly_to_face_position(LastTriggeringUnit(), PositionOfEntity(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()))),
						if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
							apply_force_on_entity_at_angle(RandomNumberBetween(3000, 6000), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							apply_force_on_entity_at_angle(RandomNumberBetween(300, 600), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					], [
						rotate_entity_instantly_to_face_position(LastTriggeringUnit(), RandomPositionInRegion(EntityBounds(LastTriggeringUnit()))),
						if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
							apply_force_on_entity_at_angle(RandomNumberBetween(1500, 3500), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							apply_force_on_entity_at_angle(RandomNumberBetween(150, 400), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						stop_using_item(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					]),
					set_entity_attribute(AttributeTypes.MOVE, LastTriggeringUnit(), RandomNumberBetween(35, 100)),
					
				], [
					
				]),
				
			]),
			
		]


@script(triggers=[])
class OpenShop():
	def _build(self):
		self.actions = [
			open_shop_for_player(Shops.FROGE_SHOP, OwnerOfEntity(LastCastingUnit())),
			
		]