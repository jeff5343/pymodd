from typing import override
from pymodd.utils.type_of_item import type_of_item
from pymodd.utils.to_dict import to_dict
from pymodd.core.base import Base

from pymodd.core.function import Function


class Entity(Function):
    def __init__(self) -> None:
        super().__init__()


class Player(Entity):
    def __init__(self) -> None:
        super().__init__()


class Unit(Entity):
    def __init__(self) -> None:
        super().__init__()


class Projectile(Entity):
    def __init__(self) -> None:
        super().__init__()


class Item(Entity):
    def __init__(self) -> None:
        super().__init__()


class Debris(Entity):
    def __init__(self) -> None:
        super().__init__()


class Position(Function):
    def __init__(self) -> None:
        super().__init__()


class Attribute(Function):
    def __init__(self) -> None:
        super().__init__()


class Sensor(Function):
    def __init__(self) -> None:
        super().__init__()


class Number(Function):
    def __init__(self, number: int):
        super().__init__()
        self.function = {
            "direct": True,
            "value": number,
        }

    # calculation functions
    def __add__(self, other):
        return Calculation(self, "+", other)

    def __sub__(self, other):
        return Calculation(self, "-", other)

    def __mul__(self, other):
        return Calculation(self, "*", other)

    def __truediv__(self, other):
        return Calculation(self, "/", other)

    def __mod__(self, other):
        return Calculation(self, "%", other)

    def __pow__(self, other):
        return Exponent(self, other)

    def __radd__(self, other):
        return Calculation(other, "+", self)

    def __rsub__(self, other):
        return Calculation(other, "-", self)

    def __rmul__(self, other):
        return Calculation(other, "*", self)

    def __rtruediv__(self, other):
        return Calculation(other, "/", self)

    def __rmod__(self, other):
        return Calculation(other, "%", self)

    def __rpow__(self, other):
        return Exponent(other, self)


class String(Function):
    def __init__(self, string: str):
        super().__init__()
        self.function = {
            "direct": True,
            "value": string,
        }

    # concat functions
    def __add__(self, other):
        return Concat(self, other)

    def __radd__(self, other):
        return Concat(other, self)


class Boolean(Function):
    def __init__(self, boolean: bool):
        super().__init__()
        self.function = {
            "direct": True,
            "value": boolean,
        }


class Object(Function):
    def __init__(self) -> None:
        super().__init__()


class Particle(Function):
    def __init__(self) -> None:
        super().__init__()


class Region(Function):
    def __init__(self) -> None:
        super().__init__()


# ---------------------------------------------------------------------------- #
#                                  Operations                                  #
# ---------------------------------------------------------------------------- #


class Condition(Function):
    """Deprecated, use python comparison operators instead"""

    def __init__(self, item_a: Base, operator: str, item_b: Base):
        super().__init__()
        self.item_a: Base = item_a
        self.operator: str = operator.upper()
        self.item_b: Base = item_b
        if self.operator == "AND" or self.operator == "OR":
            self.comparison: str = operator.lower()
        else:
            self.comparison: str = type_of_item(item_a) or type_of_item(item_b)

    @override
    def to_dict(self):
        return [
            {
                "operandType": self.comparison,
                "operator": self.operator,
            },
            to_dict(self.item_a),
            to_dict(self.item_b),
        ]


class Calculation(Number):
    """Deprecated, use python arithmetic operators instead"""

    def __init__(self, item_a: Function, operator: str, item_b: Function):
        super().__init__(0)
        self.function: str = "calculate"
        self.options = {
            "items": [
                {"operator": operator},
                to_dict(item_a),
                to_dict(item_b),
            ]
        }


class Exponent(Number):
    """Exponent operator, peprecated, use python arithmetic operators instead"""

    def __init__(self, base: Function, power: Function):
        super().__init__(0)
        self.function: str = "getExponent"
        self.options = {
            "base": to_dict(base),
            "power": to_dict(power),
        }


class Concat(String):
    """Deprecated, use python `+` operator instead"""

    def __init__(self, text_a: Function, text_b: Function):
        super().__init__("")
        self.function: str = "concat"
        self.options = {
            "textA": to_dict(text_a),
            "textB": to_dict(text_b),
        }
