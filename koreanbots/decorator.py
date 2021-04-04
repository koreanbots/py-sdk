import functools
import inspect
from typing import Any, TYPE_CHECKING, Literal, get_args

if TYPE_CHECKING:
    from .errors import AuthorizeError
    from .http import KoreanbotsRequester


def required(f: Any):
    @functools.wraps(f)
    async def decorator_function(
        self: "KoreanbotsRequester", *args: Any, **kwargs: Any
    ):
        if not self.api_key:
            raise AuthorizeError("This endpoint required koreanbots token.")

        return await f(self, *args, **kwargs)

    return decorator_function


def strict_literal(argument_name: str):
    def decorator(f: Any):
        @functools.wraps(f)
        async def decorated_function(*args: Any, **kwargs: Any):
            # First get about func args
            full_arg_spec = inspect.getfullargspec(f)
            # Get annotation
            arg_annoration = full_arg_spec.annotations[argument_name]
            # Check annotation is Lireral
            if arg_annoration.__origin__ is Literal:
                # Literal -> list
                literal_list = list(get_args(arg_annoration))
                # Get index
                arg_index = full_arg_spec.args.index(argument_name)
                # Handle arguments
                if arg_index < len(args) and args[arg_index] not in literal_list:
                    raise ValueError(
                        f"Arguments do not match. Expected: {literal_list}"
                    )
                # Handle keyword arguments
                elif kwargs.get(argument_name):
                    if kwargs[argument_name] not in literal_list:
                        raise ValueError(
                            f"Arguments do not match. Expected: {literal_list}"
                        )

            return await f(*args, **kwargs)

        return decorated_function

    return decorator
