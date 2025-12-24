from typing import Any

from pymodd.core.function import Function
from pymodd.utils.generate_random_key import generate_random_key


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
