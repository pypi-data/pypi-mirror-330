# easy-exit-calls

A Python library for managing exit handlers with enhanced features like decorators, UUID tracking, and LIFO execution.

## Features

- **Decorator Support**: Easily register functions as exit handlers using a decorator.
- **LIFO Execution**: Handlers execute in Last-In-First-Out order by default (configurable).
- **UUID Tracking**: Each handler is assigned a unique UUID for easy management.
- **Thread Safety**: Uses threading locks to ensure safe registration/unregistration.
- **Detailed Logging**: Integrated with a logging engine for debugging and tracking.
- **Error Handling**: Captures exceptions during exit and logs them with tracebacks.

## Installation

```bash
pip install easy-exit-calls
```

## Usage

### Basic Decorator Usage

```python
from easy_exit_calls import register_exit_handler

@register_exit_handler
def cleanup():
    print("Cleaning up resources...")

# Exiting the program will automatically trigger this handler.
```

### Decorator with Arguments

```python
from easy_exit_calls import register_exit_handler

@register_exit_handler("arg1", key="value")
def cleanup_with_args(arg1, key=None):
    print(f"Cleaning up with {arg1} and {key}")

# Handler called with provided args/kwargs on exit.
```

### Manual Registration

```python
from easy_exit_calls import ExitCallHandler

def manual_cleanup():
    print("Manual cleanup")

ExitCallHandler().register_handler(manual_cleanup)

# Exiting the program will manually trigger this handler.
```

### Unregistering Handlers

```python 
from easy_exit_calls import ExitCallHandler

def cleanup():
    print("Cleaning up resources...")

handler_uuid = ExitCallHandler().register_handler(cleanup)

# Unregister the handler by UUID.
ExitCallHandler().unregister_by_uuid(handler_uuid)
```

### Execution Order

```python
from easy_exit_calls import register_exit_handler

@register_exit_handler
def first_handler():
    print("First handler")

@register_exit_handler
def second_handler():
    print("Second handler")

# Output on exit:
# Second handler
# First handler
# (LIFO execution order)
```

## API Reference

### `ExitCallHandler`

Singleton class managing exit handlers.

#### Methods:

- `register_handler(func: Callable, *args, **kwargs) -> str`:
    Register a new exit handler with optional args/kwargs. Returns the UUID of the handler.<br><br>
- `unregister_by_uuid(uuid)`:
    Unregister a handler by UUID.<br><br>
- `unregister_handler(func, *args, **kwargs)`:
    Unregister a handler by function reference and optional args/kwargs.<br><br>
- `call_handlers()`:
    Manually call all registered handlers.<br><br>

### `register_exit_handler`

Decorator for registering a function as an exit handler.

#### Parameters:

- `*handler_args`:
    Optional arguments to pass to the handler function.<br><br>
- `**handler_kwargs`:
    Optional keyword arguments to pass to the handler function.<br><br>


## Contributing

Contributions are welcome! Here's how you can get started:
  1) Fork the repository.<br><br>
  2) Create a new branch (`git checkout -b feature-branch`).<br><br>
  3) Make your changes.<br><br>
  4) Commit your changes (`git commit -m 'Add feature'`).<br><br>
  5) Push your changes to your fork (`git push origin feature-branch`).<br><br>
  6) Create a pull request.<br><br>


## License

This project is released under the [MIT License](LICENSE.md).
