from typing import Any
from .type import Debris, Entity, Item, Particle, Player, Projectile, Region, Unit

import pymodd.variable_types


class SelectedEntity(Entity):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "getSelectedEntity"
        self.options = {}


class SelectedPlayer(Player):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedPlayer"
        self.options = {}


class SelectedUnit(Unit):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedUnit"
        self.options = {}


class SelectedItem(Item):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedItem"
        self.options = {}


class SelectedProjectile(Projectile):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedProjectile"
        self.options = {}


class SelectedDebris(Debris):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedDebris"
        self.options = {}


class SelectedParticle(Particle):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedParticle"
        self.options = {}


class SelectedRegion(Region):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedRegion"
        self.options = {}


class SelectedUnitType(pymodd.variable_types.UnitTypeBase):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedUnitType"
        self.options = {}


class SelectedItemType(pymodd.variable_types.ItemTypeBase):
    def __init__(self):  # pyright: ignore[reportMissingSuperCall]
        self.function: str | dict[str, Any] | None = "selectedItemType"
        self.options = {}
