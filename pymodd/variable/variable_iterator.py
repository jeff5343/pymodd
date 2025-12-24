from typing import Any
from pymodd.function.group import (
    ItemGroup,
    UnitGroup,
    PlayerGroup,
    ItemTypeGroup,
    UnitTypeGroup,
)
from pymodd.variable.data_type import DataType


def get_variable_iterating_action(variable) -> Any:
    """For group data types only. Used during script compilation"""
    if variable.data_type == DataType.ITEM_GROUP:
        return ItemGroup()._get_iterating_action()
    elif variable.data_type == DataType.UNIT_GROUP:
        return UnitGroup()._get_iterating_action()
    elif variable.data_type == DataType.PLAYER_GROUP:
        return PlayerGroup()._get_iterating_action()
    elif variable.data_type == DataType.ITEM_TYPE_GROUP:
        return ItemTypeGroup()._get_iterating_action()
    elif variable.data_type == DataType.UNIT_TYPE_GROUP:
        return UnitTypeGroup()._get_iterating_action()
    return None


def get_variable_iteration_object(variable) -> Any:
    """For group data types only. Used during script compilation"""
    if variable.data_type == DataType.ITEM_GROUP:
        return ItemGroup()._get_iteration_object()
    elif variable.data_type == DataType.UNIT_GROUP:
        return UnitGroup()._get_iteration_object()
    elif variable.data_type == DataType.PLAYER_GROUP:
        return PlayerGroup()._get_iteration_object()
    elif variable.data_type == DataType.ITEM_TYPE_GROUP:
        return ItemTypeGroup()._get_iteration_object()
    elif variable.data_type == DataType.UNIT_TYPE_GROUP:
        return UnitTypeGroup()._get_iteration_object()
    return None
