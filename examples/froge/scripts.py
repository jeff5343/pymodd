from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Script, Trigger, UiTarget, Flip

from game_variables import *


class Initialize(Script):
	def _build(self):
		self.key = 'initialize'
		self.triggers = [Trigger.GAME_START]
		self.actions = [
			assign_player_type(Variables.AI, PlayerTypes.AI),
			
		]


class PlayerJoins(Script):
	def _build(self):
		self.key = 'playerJoinsGame'
		self.triggers = [Trigger.PLAYER_JOINS_GAME]
		self.actions = [
			create_unit_for_player_at_position(UnitTypes.POOPER, LastTriggeringPlayer(), RandomPositionInRegion(EntireMapRegion()), 0),
			player_camera_track_unit(LastTriggeringPlayer(), LastCreatedUnit()),
			assign_player_type(LastTriggeringPlayer(), PlayerTypes.PLAYER),
			
		]


class PlayerLeaves(Script):
	def _build(self):
		self.key = 'playerLeavesGame'
		self.triggers = [Trigger.PLAYER_LEAVES_GAME]
		self.actions = [
			for_all_units(AllUnitsOwnedByPlayer(LastTriggeringPlayer()), [
				destroy_entity(SelectedUnit()),
				
			], comment='when a player leaves, destroy all units owned by that player'),
			
		]


class EverySecond(Script):
	def _build(self):
		self.key = 'P8MwXcSxq7'
		self.triggers = [Trigger.EVERY_SECOND]
		self.actions = [
			if_else((NumberOfUnitsOfUnitType(UnitTypes.FROG) < 5), [
				create_unit_for_player_at_position(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
				
			], [
				if_else((NumberOfUnitsOfUnitType(UnitTypes.FROG_BOSS) == 0), [
					if_else((Variables.BOSS_TIMER <= 0), [
						create_unit_for_player_at_position(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
						update_ui_text_for_time_for_player(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000),
						
					], [
						
					]),
					decrease_variable_by_number(Variables.BOSS_TIMER, 1),
					
				], [
					
				]),
				
			]),
			
		]


class WhenAUnitsAttributeBecomes0OrLess(Script):
	def _build(self):
		self.key = 'CE0PBg1VWG'
		self.triggers = [Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO]
		self.actions = [
			if_else((AttributeTypeOfAttribute(TriggeringAttribute()) == AttributeTypes.HEALTH), [
				if_else((PlayerTypeOfPlayer(OwnerOfEntity(LastTriggeringUnit())) == PlayerTypes.PLAYER), [
					set_entity_attribute(AttributeTypes.HEALTH, LastTriggeringUnit(), EntityAttributeMax(AttributeTypes.HEALTH, LastTriggeringUnit())),
					set_entity_variable(LastTriggeringUnit(), EntityVariables.TARGET_UNIT, Undefined()),
					move_entity(LastTriggeringUnit(), CenterOfRegion(EntireMapRegion())),
					
				], [
					if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
						set_variable(Variables.BOSS_TIMER, 200),
						set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 7),
						
					], [
						set_player_attribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 1),
						
					]),
					destroy_entity(LastTriggeringUnit()),
					
				]),
				
			], [
				if_else((AttributeTypeOfAttribute(TriggeringAttribute()) == AttributeTypes.MOVE), [
					set_entity_variable(LastTriggeringUnit(), EntityVariables.TARGET_UNIT, Undefined()),
					for_all_entities(EntitiesInRegion(DynamicRegion(PositionX(EntityPosition(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), PositionY(EntityPosition(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()) / 2), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()))), [
						if_else((PlayerTypeOfPlayer(OwnerOfEntity(SelectedEntity())) == PlayerTypes.PLAYER), [
							if_else(((ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()) == Undefined()) | (DistanceBetweenPositions(EntityPosition(SelectedEntity()), EntityPosition(LastTriggeringUnit())) > DistanceBetweenPositions(EntityPosition(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit())), EntityPosition(LastTriggeringUnit())))), [
								create_floating_text('Froge sense', EntityPosition(LastTriggeringUnit()), '#327117', disabled=True),
								set_entity_variable(LastTriggeringUnit(), EntityVariables.TARGET_UNIT, SelectedEntity()),
								
							], [
								
							]),
							
						], [
							
						]),
						
					]),
					if_else((ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()) != Undefined()), [
						rotate_entity_to_face_position(LastTriggeringUnit(), EntityPosition(ValueOfEntityVariable(EntityVariables.TARGET_UNIT, LastTriggeringUnit()))),
						if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
							apply_force_on_entity_angle(RandomNumberBetween(3000, 6000), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							apply_force_on_entity_angle(RandomNumberBetween(300, 600), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						start_using_item(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					], [
						rotate_entity_to_face_position(LastTriggeringUnit(), RandomPositionInRegion(EntityBounds(LastTriggeringUnit()))),
						if_else((UnitTypeOfUnit(LastTriggeringUnit()) == UnitTypes.FROG_BOSS), [
							apply_force_on_entity_angle(RandomNumberBetween(1500, 3500), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							apply_force_on_entity_angle(RandomNumberBetween(150, 400), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						stop_using_item(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					]),
					set_entity_attribute(AttributeTypes.MOVE, LastTriggeringUnit(), RandomNumberBetween(35, 100)),
					
				], [
					
				]),
				
			]),
			
		]


class OpenShop(Script):
	def _build(self):
		self.key = '5BUXtByxVf'
		self.triggers = []
		self.actions = [
			open_shop_for_player(Shops.FROGE_SHOP, OwnerOfEntity(LastCastingUnit())),
			
		]