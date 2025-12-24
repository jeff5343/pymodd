from typing import Any
from caseconverter import camelcase
from pymodd.core.base import Base


def type_of_item(item: Any) -> str:
    primitive_to_type = {
        int: "number",
        float: "number",
        complex: "number",
        bool: "boolean",
        str: "string",
    }

    if primitive := primitive_to_type.get(type(item)):
        return primitive
    if isinstance(item, Base):
        base_classes = item.__class__.mro()
        for i, base_class in enumerate(base_classes):
            # TODO: find better way to do this? this is hacky
            if "VariableType" == base_class.__name__:
                if hasattr(item, "data_type"):
                    return (
                        item.data_type.value  # pyright: ignore[reportAttributeAccessIssue]
                    )
                return camelcase(base_classes[i - 1].__name__)

            if "Function" == base_class.__name__:
                if (
                    item.function  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
                    == "undefinedValue"
                ):
                    return ""
                return camelcase(base_classes[i - 1].__name__)
    print("uh oh")
    return ""
