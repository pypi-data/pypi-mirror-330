import inspect
from typing import Any, Callable, Dict


def prepare_keyword_arguments(callable_obj: Callable, kwargs_dict: Dict[str, Any]):
    """Analyze a callable to get its arguments and compare them to a dict of
    available arguments.
    Reduce the dict down to a set of keys that the callable can actually be called
    with. Any extra keys are dropped with a warning."""
    signature = inspect.signature(callable_obj)
    parameters = signature.parameters

    if any(
        parameter.kind == inspect.Parameter.VAR_KEYWORD
        for parameter in parameters.values()
    ):
        # if any of the callable's parameters use the form **kwargs,
        # then we don't need to check further, just pass everything,
        return kwargs_dict

    valid_kwargs = {}
    for key, value in kwargs_dict.items():
        if key in parameters:  # only proceed if the parameter exists on the callable
            valid_kwargs[key] = value
        else:
            print(
                f"WARNING: Ignoring job parameter: {key}. "
                "The entry point cannot receive it."
            )

    return valid_kwargs
