from inspect import isclass
from typing import (
    Any,
    Literal,
    Mapping,
    Self,
    Union,
    cast,
    get_args,
    get_origin,
    get_type_hints,
)


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
                # Handle Literal fields (e.g. Status, State) — keep value as-is
                if origin_type is Literal:
                    pass
                # Handle optional fields
                elif origin_type is Union and type(None) in get_args(type_hint):
                    # arg_type may itself be Literal; only call it if it's a plain class
                    if isclass(arg_type):
                        value = arg_type(value) if value is not None else None
                # Handle list fields
                elif origin_type is list:
                    if isclass(arg_type) and issubclass(arg_type, Deserializer):
                        value = (
                            [
                                arg_type.from_dict(cast(Mapping[str, Any], v))
                                if isinstance(v, Mapping)
                                else v
                                for v in value
                            ]
                            if value is not None
                            else []
                        )
                    elif arg_type is int:
                        value = [int(v) for v in value]
                    # Literal or other non-class arg types — keep as-is
            elif isclass(type_hint) and issubclass(type_hint, Deserializer):
                value = type_hint.from_dict(value)
            elif isclass(type_hint):
                value = type_hint(value)
            # Non-class type_hint without get_origin (shouldn't happen) — keep as-is
            converted_data[key] = value

        return cls(**converted_data)
