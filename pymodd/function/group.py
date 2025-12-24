from typing import override
from pymodd.core.function import Function
from .selected_entity import (
    SelectedDebris,
    SelectedEntity,
    SelectedItemType,
    SelectedPlayer,
    SelectedRegion,
    SelectedUnit,
    SelectedProjectile,
    SelectedItem,
    SelectedUnitType,
)
import pymodd.actions


class Group(Function):
    def _get_iterating_action(self):
        raise NotImplementedError("_get_iteration_object not implemented")

    def _get_iteration_object(self):
        raise NotImplementedError("_get_iteration_object not implemented")


class EntityGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_entities_in

    @override
    def _get_iteration_object(self):
        return SelectedEntity()


class UnitGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_units_in

    @override
    def _get_iteration_object(self):
        return SelectedUnit()


class ProjectileGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_projectiles_in

    @override
    def _get_iteration_object(self):
        return SelectedProjectile()


class ItemGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_items_in

    @override
    def _get_iteration_object(self):
        return SelectedItem()


class PlayerGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_players_in

    @override
    def _get_iteration_object(self):
        return SelectedPlayer()


class ItemTypeGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_item_types_in

    @override
    def _get_iteration_object(self):
        return SelectedItemType()


class UnitTypeGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_unit_types_in

    @override
    def _get_iteration_object(self):
        return SelectedUnitType()


class DebrisGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_debris_in

    @override
    def _get_iteration_object(self):
        return SelectedDebris()


class RegionGroup(Group):
    @override
    def _get_iterating_action(self):
        return pymodd.actions.for_all_regions_in

    @override
    def _get_iteration_object(self):
        return SelectedRegion()
