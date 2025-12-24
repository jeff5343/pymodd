from typing import Any

from pymodd.core.function import Function
from pymodd.function.type import Calculation, Concat, Exponent
from pymodd.utils.generate_random_key import generate_random_key
from pymodd.utils.type_of_item import type_of_item
from pymodd.variable.data_type import DataType


class VariableType(Function):
    def __init__(self, id: str | None = None, **data_path_to_new_values_kwargs) -> None:
        """
        Args:
        id: id of the variable. will be generated if none is given
        **data_path_to_new_values_kwargs: key represents the path to the value in JSON, value represents the new value.
            Example: data['key1']['key2'] = 1 => key1_key2 = 1
            Check updated_data_with_user_provided_values for its use case.
        """
        super().__init__()
        self.id = generate_random_key() if id is None else id
        self.data_type: DataType | None = None
        self.data_keys_to_new_values = data_path_to_new_values_kwargs.items()
        self.function = {
            "direct": True,
            "value": self.id,
        }

    def updated_data_with_user_provided_values(
        self, data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Updates the passed in variable data with user provided values from data_key_to_new_values.
        Example:
            ItemTypeBase('RAND_ID', delayBeforeUse=5, bulletStartPosition_rotation = 180) ->
            data_keys_to_new_values = {'delayBeforeUse': 5, 'bulletStartPosition_rotation': 180} ->
            data['delayBeforeUse'] = 5
            data['bulletStartPosition']['rotation'] = 180
        """
        for path_to_old, new_value in self.data_keys_to_new_values:
            keys = str(path_to_old).split("_")
            d = data
            for i, path_to_old in enumerate(keys):
                if i == len(keys) - 1:
                    d[path_to_old] = new_value
                d = d[path_to_old]
        return data

    def get_template_data(self) -> dict[str, Any]:
        raise NotImplementedError("get_template_data method not implemented")

    # calculation functions
    def __add__(self, other):
        if "string" in [type_of_item(self).lower(), type_of_item(other).lower()]:
            return Concat(self, other)
        else:
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
        if "string" in [type_of_item(self).lower(), type_of_item(other).lower()]:
            return Concat(other, self)
        else:
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
