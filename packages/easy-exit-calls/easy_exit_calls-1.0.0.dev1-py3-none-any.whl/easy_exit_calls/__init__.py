"""
This module provides a simple way to register exit handlers for your Python applications.

The main class is ExitCallHandler, which is used to register and manage exit handlers.

Included is a decorator, register_exit_handler, which can be used to register an exit handler for a function. This is a
convenient way to register exit handlers for functions.

Example:
    >>> from easy_exit_calls import register_exit_handler, ExitCallHandler
    >>>
    >>> @register_exit_handler()
    ... def my_exit_handler():
    ...     print("Exiting...")
    ...
    >>> # Create an instance of ExitCallHandler
    >>> eh = ExitCallHandler()
    >>>
    >>> # Register an exit handler
    >>> eh.register_handler(my_exit_handler)
    >>>
    >>> # Call the exit handlers
    >>> eh.call_handlers()
    Exiting...
"""

from easy_exit_calls.classes import ExitCallHandler
from easy_exit_calls.decorator import register_exit_handler

__all__ = [
    'ExitCallHandler',
    'register_exit_handler',
]
