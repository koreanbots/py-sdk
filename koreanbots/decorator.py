import functools
import inspect
from typing import Any, Callable, List, Literal, cast, get_args

from koreanbots.typing import CORO


def strict_literal(argument_names: List[str]) -> Callable[[CORO], CORO]:
    def decorator(f: CORO) -> CORO:
        @functools.wraps(f)
        async def decorated_function(*args: Any, **kwargs: Any) -> Any:
            # First get about func args
            full_arg_spec = inspect.getfullargspec(f)
            for argument_name in argument_names:
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
                    elif (
                        kwargs.get(argument_name)
                        and kwargs[argument_name] not in literal_list
                    ):
                        if kwargs[argument_name] not in literal_list:
                            raise ValueError(
                                f"Arguments do not match. Expected: {literal_list}"
                            )

            return await f(*args, **kwargs)

        return cast(CORO, decorated_function)

    return decorator
