"""
This module contains the decorator function to register an exit handler with the ExitCallHandler.

The decorator function is register_exit_handler, which can be used to register an exit handler for a function. This is a
convenient way to register exit handlers for functions.

Example:
    >>> from easy_exit_calls import register_exit_handler
    >>>
    >>> @register_exit_handler()
    ... def my_exit_handler():
    ...     print("Exiting...")
    ...
    >>> # Call the exit handlers
    >>> # Press Ctrl+D
    Exiting...

Since:
    1.0.0
"""


def register_exit_handler(*args, **kwargs):
    """
    Register an exit handler with the ExitCallHandler.

    Parameters:
        *handler_args:
            Positional arguments to pass to the handler function.

        **handler_kwargs:
            Keyword arguments to pass to the handler function.
    """
    from easy_exit_calls import ExitCallHandler

    # Case 1: Decorator used without parentheses (@register_exit_handler)
    if len(args) == 1 and callable(args[0]):
        func = args[0]  # Get the function being decorated
        ExitCallHandler().register_handler(func)  # Register with no arguments
        return func

    # Case 2: Decorator used with arguments (@register_exit_handler(*args, **kwargs))
    def decorator(func):
        ExitCallHandler().register_handler(func, *args, **kwargs)
        return func

    return decorator


__all__ = ['register_exit_handler']
