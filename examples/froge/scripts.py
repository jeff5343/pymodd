from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Script, Trigger, UiTarget, Flip

from game_variables import *


class Initialize(Script):
	def _build(self):
		self.key = 'initialize'
		self.triggers = [Trigger.GAME_START]
		self.actions = [
			AssignPlayerType(Variables.AI, PlayerTypes.AI),
			
		]


class PlayerJoins(Script):
	def _build(self):
		self.key = 'playerJoinsGame'
		self.triggers = [Trigger.PLAYER_JOINS_GAME]
		self.actions = [
			CreateUnitForPlayerAtPosition(UnitTypes.POOPER, LastTriggeringPlayer(), RandomPositionInRegion(EntireMapRegion()), 0),
			PlayerCameraTrackUnit(LastTriggeringPlayer(), LastCreatedUnit()),
			AssignPlayerType(LastTriggeringPlayer(), PlayerTypes.PLAYER),
			
		]


class PlayerLeaves(Script):
	def _build(self):
		self.key = 'playerLeavesGame'
		self.triggers = [Trigger.PLAYER_LEAVES_GAME]
		self.actions = [
			ForAllUnits(AllUnitsOwnedByPlayer(LastTriggeringPlayer()), [
				DestroyEntity(SelectedUnit()),
				
			]),
			
		]


class EverySecond(Script):
	def _build(self):
		self.key = 'P8MwXcSxq7'
		self.triggers = [Trigger.EVERY_SECOND]
		self.actions = [
			IfStatement(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG), '<', 5), [
				CreateUnitForPlayerAtPosition(UnitTypes.FROG, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
				
			], [
				IfStatement(Condition(NumberOfUnitsOfUnitType(UnitTypes.FROG_BOSS), '==', 0), [
					IfStatement(Condition(Variables.BOSS_TIMER, '<=', 0), [
						CreateUnitForPlayerAtPosition(UnitTypes.FROG_BOSS, Variables.AI, RandomPositionInRegion(EntireMapRegion()), 0),
						UpdateUiTextForTimeForPlayer(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000),
						
					], [
						
					]),
					DecreaseVariableByNumber(Variables.BOSS_TIMER, 1),
					
				], [
					
				]),
				
			]),
			
		]


class WhenAUnitsAttributeBecomes0OrLess(Script):
	def _build(self):
		self.key = 'CE0PBg1VWG'
		self.triggers = [Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO]
		self.actions = [
			IfStatement(Condition(AttributeTypeOfAttribute(TriggeringAttribute()), '==', AttributeTypes.HEALTH), [
				IfStatement(Condition(PlayerTypeOfPlayer(OwnerOfEntity(LastTriggeringUnit())), '==', PlayerTypes.PLAYER), [
					SetEntityAttribute(AttributeTypes.HEALTH, LastTriggeringUnit(), EntityAttributeMax(AttributeTypes.HEALTH, LastTriggeringUnit())),
					SetEntityVariable(LastTriggeringUnit(), PlayerVariables.TARGET_UNIT, Undefined()),
					MoveEntity(LastTriggeringUnit(), CenterOfRegion(EntireMapRegion())),
					
				], [
					IfStatement(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '==', UnitTypes.FROG_BOSS), [
						SetVariable(Variables.BOSS_TIMER, 200),
						SetPlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), Calculate(PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())), '+', 7)),
						
					], [
						SetPlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), Calculate(PlayerAttribute(AttributeTypes.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())), '+', 1)),
						
					]),
					DestroyEntity(LastTriggeringUnit()),
					
				]),
				
			], [
				IfStatement(Condition(AttributeTypeOfAttribute(TriggeringAttribute()), '==', AttributeTypes.MOVE), [
					SetEntityVariable(LastTriggeringUnit(), PlayerVariables.TARGET_UNIT, Undefined()),
					ForAllEntities(EntitiesInRegion(DynamicRegion(Calculate(PositionX(EntityPosition(LastTriggeringUnit())), '-', Calculate(ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), '/', 2)), Calculate(PositionY(EntityPosition(LastTriggeringUnit())), '-', Calculate(ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), '/', 2)), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()), ValueOfEntityVariable(EntityVariables.SENSOR_RADIUS, LastTriggeringUnit()))), [
						IfStatement(Condition(PlayerTypeOfPlayer(OwnerOfEntity(SelectedEntity())), '==', PlayerTypes.PLAYER), [
							IfStatement(Condition(Condition(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit()), '==', Undefined()), 'OR', Condition(DistanceBetweenPositions(EntityPosition(SelectedEntity()), EntityPosition(LastTriggeringUnit())), '>', DistanceBetweenPositions(EntityPosition(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit())), EntityPosition(LastTriggeringUnit())))), [
								CreateFloatingText('Froge sense', EntityPosition(LastTriggeringUnit()), '#327117'),
								SetEntityVariable(LastTriggeringUnit(), PlayerVariables.TARGET_UNIT, SelectedEntity()),
								
							], [
								
							]),
							
						], [
							
						]),
						
					]),
					IfStatement(Condition(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit()), '!=', Undefined()), [
						RotateEntityToFacePosition(LastTriggeringUnit(), EntityPosition(ValueOfEntityVariable(PlayerVariables.TARGET_UNIT, LastTriggeringUnit()))),
						IfStatement(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '==', UnitTypes.FROG_BOSS), [
							ApplyForceOnEntityAngle(RandomNumberBetween(3000, 6000), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							ApplyForceOnEntityAngle(RandomNumberBetween(300, 600), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						StartUsingItem(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					], [
						RotateEntityToFacePosition(LastTriggeringUnit(), RandomPositionInRegion(EntityBounds(LastTriggeringUnit()))),
						IfStatement(Condition(UnitTypeOfUnit(LastTriggeringUnit()), '==', UnitTypes.FROG_BOSS), [
							ApplyForceOnEntityAngle(RandomNumberBetween(1500, 3500), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						], [
							ApplyForceOnEntityAngle(RandomNumberBetween(150, 400), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit())),
							
						]),
						StopUsingItem(ItemCurrentlyHeldByUnit(LastTriggeringUnit())),
						
					]),
					SetEntityAttribute(AttributeTypes.MOVE, LastTriggeringUnit(), RandomNumberBetween(35, 100)),
					
				], [
					
				]),
				
			]),
			
		]


class OpenShop(Script):
	def _build(self):
		self.key = '5BUXtByxVf'
		self.triggers = []
		self.actions = [
			OpenShopForPlayer(Shops.FROGE_SHOP, OwnerOfEntity(LastCastingUnit())),
			
		]