import functools
from typing import Literal, get_args
from koreanbots.http import KoreanbotsRequester
from koreanbots.errors import AuthorizeError
import inspect


def required(f):
    @functools.wraps(f)
    async def decorator_function(self: KoreanbotsRequester, *args, **kwargs):
        if not self.api_key:
            raise AuthorizeError("This endpoint required koreanbots token.")

        return await f(self, *args, **kwargs)

    return decorator_function


def strict_literal(argument_name: str):
    def decorator(f):
        @functools.wraps(f)
        async def decorated_function(*args, **kwargs):
            # First get about func args
            full_arg_spec = inspect.getfullargspec(f)
            # Get annotation
            arg_annoration = full_arg_spec.annotations[argument_name]
            # Check annotation is Lireral
            if arg_annoration.__origin__ is Literal:
                # Literal -> Tuple
                literal_list = list(get_args(arg_annoration))
                # Get index
                arg_index = full_arg_spec.args.index(argument_name)
                # Handle arguments
                if arg_index < len(args) and args[arg_index] not in literal_list:
                    raise ValueError(
                        f"Arguments do not match. Expected: {literal_list}"
                    )
                # Handle keyword arguments
                elif recive_arg := kwargs.get(argument_name):
                    if recive_arg not in literal_list:
                        raise ValueError(
                            f"Arguments do not match. Expected: {literal_list}"
                        )

            return await f(*args, **kwargs)

        return decorated_function

    return decorator
