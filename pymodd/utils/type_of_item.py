from typing import Any
from caseconverter import camelcase
from pymodd.core.function import Function

import pymodd.variable_types


def type_of_item(item: Any):
    primitive_to_type = {
        int: "number",
        float: "number",
        complex: "number",
        bool: "boolean",
        str: "string",
    }

    if primitive := primitive_to_type.get(type(item)):
        return primitive
    if isinstance(item, pymodd.variable_types.VariableBase):
        return item.data_type.value
    if isinstance(item, pymodd.variable_types.VariableType):
        base_classes = item.__class__.mro()
        for i, base_class in enumerate(base_classes):
            if base_class.__name__ == "pymodd.variable_types.VariableType":
                return camelcase(base_classes[i - 1].__name__)
    if isinstance(item, Function):
        if item.function == "undefinedValue":
            return ""

        base_classes = item.__class__.mro()
        for i, base_class in enumerate(base_classes):
            if base_class.__name__ == "Function":
                return camelcase(base_classes[i - 1].__name__)
    return ""
