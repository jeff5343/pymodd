from pymodd.actions import *
from pymodd.functions import *
from pymodd.script import Trigger, UiTarget, Flip, script

from game_variables import *


@script(triggers=[Trigger.GAME_START])
def initialize():
    assign_player_to_player_type(Variable.AI, PlayerType.AI)


@script(triggers=[Trigger.PLAYER_JOINS_GAME])
def player_joins():
    create_unit_for_player_at_position_with_rotation(UnitType.USER, LastTriggeringPlayer(), RandomPositionInRegion(EntireMapRegion()), 0)
    make_camera_of_player_track_unit(LastTriggeringPlayer(), LastCreatedUnit())
    assign_player_to_player_type(LastTriggeringPlayer(), PlayerType.PLAYER)


@script(triggers=[Trigger.PLAYER_LEAVES_GAME])
def player_leaves():
    for unit in AllUnitsOwnedByPlayer(LastTriggeringPlayer()):
        destroy_entity(unit)


@script(triggers=[Trigger.EVERY_SECOND])
def every_second():
    if NumberOfUnitsOfUnitType(UnitType.FROG) < 5:
        create_unit_for_player_at_position_with_rotation(UnitType.FROG, Variable.AI, RandomPositionInRegion(EntireMapRegion()), 0)
    else:
        if NumberOfUnitsOfUnitType(UnitType.FROG_BOSS) == 0:
            if Variable.BOSS_TIMER <= 0:
                create_unit_for_player_at_position_with_rotation(UnitType.FROG_BOSS, Variable.AI, RandomPositionInRegion(EntireMapRegion()), 0)
                update_ui_target_for_player_for_miliseconds(UiTarget.CENTER, 'BOSS SPAWNED', Undefined(), 5000)
            decrease_variable_by_number(Variable.BOSS_TIMER, 1)


@script(triggers=[Trigger.UNIT_ATTRIBUTE_BECOMES_ZERO])
def when_a_units_attribute_becomes_0_or_less():
    if AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeType.HEALTH:
        if PlayerTypeOfPlayer(OwnerOfEntity(LastTriggeringUnit())) == PlayerType.PLAYER:
            set_entity_attribute(AttributeType.HEALTH, LastTriggeringUnit(), AttributeMaxOfEntity(AttributeType.HEALTH, LastTriggeringUnit()))
            set_entity_variable(EntityVariable.TARGET_UNIT, LastTriggeringUnit(), Undefined())
            move_entity_to_position(LastTriggeringUnit(), CenterOfRegion(EntireMapRegion()))
        else:
            if UnitTypeOfUnit(LastTriggeringUnit()) == UnitType.FROG_BOSS:
                set_variable(Variable.BOSS_TIMER, 200)
                set_player_attribute(AttributeType.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), ValueOfPlayerAttribute(AttributeType.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 7)
            else:
                set_player_attribute(AttributeType.FROG_KILLS, OwnerOfEntity(LastAttackingUnit()), ValueOfPlayerAttribute(AttributeType.FROG_KILLS, OwnerOfEntity(LastAttackingUnit())) + 1)
            destroy_entity(LastTriggeringUnit())
    else:
        if AttributeTypeOfAttribute(LastTriggeringAttribute()) == AttributeType.MOVE:
            set_entity_variable(EntityVariable.TARGET_UNIT, LastTriggeringUnit(), Undefined())
            for entity in AllEntitiesInRegion(DynamicRegion(XCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariable.SENSOR_RADIUS, LastTriggeringUnit()) / 2), YCoordinateOfPosition(PositionOfEntity(LastTriggeringUnit())) - (ValueOfEntityVariable(EntityVariable.SENSOR_RADIUS, LastTriggeringUnit()) / 2), ValueOfEntityVariable(EntityVariable.SENSOR_RADIUS, LastTriggeringUnit()), ValueOfEntityVariable(EntityVariable.SENSOR_RADIUS, LastTriggeringUnit()))):
                if PlayerTypeOfPlayer(OwnerOfEntity(entity)) == PlayerType.PLAYER:
                    if ValueOfEntityVariable(EntityVariable.TARGET_UNIT, LastTriggeringUnit()) == Undefined() or DistanceBetweenPositions(PositionOfEntity(entity), PositionOfEntity(LastTriggeringUnit())) > DistanceBetweenPositions(PositionOfEntity(ValueOfEntityVariable(EntityVariable.TARGET_UNIT, LastTriggeringUnit())), PositionOfEntity(LastTriggeringUnit())):
                        create_floating_text_at_position_with_color('Froge sense', PositionOfEntity(LastTriggeringUnit()), '#327117', disabled=True)
                        set_entity_variable(EntityVariable.TARGET_UNIT, LastTriggeringUnit(), entity)
            if ValueOfEntityVariable(EntityVariable.TARGET_UNIT, LastTriggeringUnit()) != Undefined():
                rotate_entity_instantly_to_face_position(LastTriggeringUnit(), PositionOfEntity(ValueOfEntityVariable(EntityVariable.TARGET_UNIT, LastTriggeringUnit())))
                if UnitTypeOfUnit(LastTriggeringUnit()) == UnitType.FROG_BOSS:
                    apply_force_on_entity_at_angle(RandomNumberBetween(3000, 6000), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
                else:
                    apply_force_on_entity_at_angle(RandomNumberBetween(300, 600), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
                use_item_continuously_until_stopped(ItemCurrentlyHeldByUnit(LastTriggeringUnit()))
            else:
                rotate_entity_instantly_to_face_position(LastTriggeringUnit(), RandomPositionInRegion(EntityBounds(LastTriggeringUnit())))
                if UnitTypeOfUnit(LastTriggeringUnit()) == UnitType.FROG_BOSS:
                    apply_force_on_entity_at_angle(RandomNumberBetween(1500, 3500), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
                else:
                    apply_force_on_entity_at_angle(RandomNumberBetween(150, 400), LastTriggeringUnit(), UnitsFacingAngle(LastTriggeringUnit()))
                stop_using_item(ItemCurrentlyHeldByUnit(LastTriggeringUnit()))
            set_entity_attribute(AttributeType.MOVE, LastTriggeringUnit(), RandomNumberBetween(35, 100))


@script(triggers=[])
def open_shop():
    open_shop_for_player(Shop.FROGE_SHOP, OwnerOfEntity(LastCastingUnit()))

