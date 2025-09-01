from inspect import isclass
from typing import Any, Mapping, Self, Union, get_args, get_origin, get_type_hints


class Deserializer:
    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        converted_data: dict[str, Any] = {}
        type_hints = get_type_hints(cls)

        for key, value in data.items():
            type_hint = type_hints.get(key)

            # Check for unexpected keys
            if type_hint is None:
                raise ValueError(f"Unexpected key: {key}")

            # Handle Generics
            if origin_type := get_origin(type_hint):
                arg_type = get_args(type_hint)[0]
                # Handle optional fields
                if origin_type is Union and type(None) in get_args(type_hint):
                    value = arg_type(value)
                # Handle list fields
                elif origin_type is list:
                    if isclass(arg_type) and issubclass(arg_type, Deserializer):
                        if value is None:
                            value = []
                        else:
                            value = [arg_type.from_dict(v) for v in value]
                    elif arg_type is int:
                        value = [int(v) for v in value]
            elif isclass(type_hint) and issubclass(type_hint, Deserializer):
                value = type_hint.from_dict(value)
            else:
                value = type_hint(value)
            converted_data[key] = value

        return cls(**converted_data)
