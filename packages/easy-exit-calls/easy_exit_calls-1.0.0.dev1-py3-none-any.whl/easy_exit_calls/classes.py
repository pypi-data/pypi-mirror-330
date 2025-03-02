import atexit
import threading
import traceback
from uuid import uuid4, UUID
from easy_exit_calls.log_engine import ROOT_LOGGER, Loggable
from easy_exit_calls.helpers.handler_list import HandlerList

MOD_LOGGER = ROOT_LOGGER.get_child('components.exit_calls')


class ExitCallHandler(Loggable):
    """
    A singleton class for managing exit handlers that are executed when the program terminates.

    This class allows registration, execution, and removal of exit handlers. Handlers can be executed in
    **either** LIFO (Last-In-First-Out) or FIFO (First-In-First-Out) order. It integrates with Python's `atexit`
    module to ensure handlers are executed upon normal program termination.

    Properties:
        fifo (bool):
            If True, handlers execute in FIFO order; otherwise, LIFO.

        handler_keys (list):
            A list of unique keys representing registered handlers.

        handlers (list):
            A list of registered handlers.

        handler_uuids (list):
            A list of UUIDs for registered handlers.

        lifo (bool):
            Indicates whether handlers execute in LIFO order.

        registered_with_atexit (bool):
            Indicates whether the handler is registered with `atexit`.

    Methods:
        call_handlers():
            Executes all registered exit handlers.

        clear_handlers():
            Removes all registered exit handlers.

        find_handler_by_uuid(uuid):
            Retrieves a handler by its UUID.

        function_registered(func):
            Checks if a function is already registered as an exit handler.

        has_key(key):
            Determines if a handler with a given key exists.

        has_uuid(uuid):
            Determines if a handler with a given UUID exists.

        register_handler(func, *args, return_func=False, **kwargs):
            Registers a function as an exit handler.

        register_self_with_atexit():
            Registers the handler with Python’s `atexit` module.

        unregister_all():
            Unregisters all exit handlers.

        unregister_all_with_name(name):
            Unregisters all handlers with a specific name.

        unregister_by_uuid(uuid):
            Removes a registered handler by UUID.

        unregister_handler(func, *args, **kwargs):
            Unregisters a specific exit handler by function reference and arguments.

        unregister_self_with_atexit():
            Removes this handler from Python’s `atexit` module.

    Example Usage:
        ```python
        handler = ExitCallHandler()

        def cleanup():
            print("Cleaning up!")

        handler.register_handler(cleanup)
        ```
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ExitCallHandler, cls).__new__(cls, *args, **kwargs)
            # Use a list to store handler dictionaries
            cls._instance._handlers = HandlerList(
                on_empty=cls._instance.unregister_self_with_atexit,
                on_non_empty=cls._instance.register_self_with_atexit
            )

            cls._instance._lifo = True
            cls._instance._lock = threading.Lock()

            # Register cleanup method to run on exit
            atexit.register(cls._instance._cleanup)

        return cls._instance

    def __init__(self, fifo=False):

        self.__registered_with_atexit = False

        if isinstance(fifo, bool) and fifo:
            self._lifo = False


        if not hasattr(self, '_initialized'):
            super().__init__(MOD_LOGGER)
            self._initialized = True

    def _check_for_key(self, key):
        """
        Checks if a key already exists in the registered handlers.

        Parameters:
            key (tuple):
            A tuple containing the function, arguments, and keyword arguments of the handler.

        Returns:
            bool:
                True if the key exists, False otherwise.
        """
        for entry in self.handlers:
            existing_key = self._get_key(entry['func'], entry['args'], entry['kwargs'])
            if existing_key == key:
                return True

    def _cleanup(self):
        """
        Executes all registered exit handlers.
        """
        log = self.method_logger

        handlers = reversed(self._handlers) if self.lifo else self._handlers

        for entry in list(handlers):
            name = ''
            if 'handler_info' in entry:
                info = entry['handler_info']
                # Build a name based on module and function name
                name = f"{info.get('module', '')}."
                if info.get('name'):
                    name += info['name']
                else:
                    name = "Unknown"

            log.debug(f"Running exit handler {name}")

            func = entry['func']
            args = entry['args']
            kwargs = entry['kwargs']

            log.debug(f"Running exit handler {name} | Function: {func} | Args: {args} | Kwargs: {kwargs}")

            try:
                func(*args, **kwargs)
            except Exception as e:
                log.error(f"Error while running exit handler {func}: {e}")
                log.debug(f"Traceback:\n{traceback.format_exc()}")
                raise e from e

    def _get_key(self, func: callable, args: tuple, kwargs: dict):
        """
        Create a unique key from a function, its arguments, and keyword arguments.

        Parameters:
            func (callable):
                The function to be called.

            args (tuple):
                Positional arguments to be passed to the function.

            kwargs (dict):
                Keyword arguments to be passed to the function.

        Returns:
            tuple:
                A tuple containing the function, arguments, and keyword arguments.
        """
        return (func, args, frozenset(kwargs.items()))

    @property
    def fifo(self) -> bool:
        """
        Get the FIFO mode for the handler.

        Returns:
            bool:
                True if FIFO mode is enabled, False otherwise.

        """
        return not self._lifo

    @fifo.setter
    def fifo(self, new: bool) -> None:
        """
        Set the FIFO mode for the handler.

        Parameters:
            new (bool):
                True to set FIFO mode, False to set LIFO mode.

        Returns:
            None

        Raises:
            TypeError:
                If the new value is not a boolean.
        """
        if not isinstance(new, bool):
            raise TypeError("fifo must be a boolean")

        self._lifo = not new

    @property
    def handler_keys(self) -> list[tuple]:
        """
        Returns a list of tuples containing the keys for all registered handlers.

        Returns:
            list[tuple]:
                A list of tuples containing the keys for all registered handlers;
                each tuple contains the function, arguments, and keyword arguments.
        """
        return [self._get_key(entry['func'], entry['args'], entry['kwargs']) for entry in self.handlers]

    @property
    def handlers(self) -> HandlerList:
        """
        Returns a list of dictionaries representing the registered exit handlers.

        Returns:
            HandlerList:
                A list of dictionaries representing the registered exit handlers.
        """
        return self._handlers

    @property
    def handler_uuids(self) -> list[UUID]:
        """
        Returns a list of UUIDs for all registered handlers.

        Returns:
            list[UUID]:
                A list of UUIDs for all registered handlers.
        """
        return [entry.get('uuid') for entry in self.handlers]

    @property
    def lifo(self):
        """
        Get the LIFO status of the exit call handler.

        Returns:
            bool: True if the exit call handler is in LIFO mode, False otherwise.
        """
        return self._lifo

    @lifo.setter
    def lifo(self, new) -> None:
        """
        Set the LIFO status of the exit call handler.

        If the value is True, handlers will execute in LIFO order. If False, handlers will execute in FIFO order.

        Parameters:
            new (bool):
                The new LIFO status to set.

        Returns:
            None
        """
        if not isinstance(new,bool):
            raise ValueError("lifo must be a boolean")

        self._lifo = new

    @property
    def registered_with_atexit(self) -> bool:
        """
        Indicates whether the handler is registered with the `atexit` module.

        Returns:
            bool:
                True if the handler is registered with `atexit`, False otherwise.
        """
        return self.__registered_with_atexit

    def call_handlers(self) -> None:
        """
        Calls all registered exit handlers.

        Returns:
            None
        """
        log = self.method_logger

        if not self.handlers:
            log.warning("No exit handlers registered")
            return

        log.debug("Calling exit handlers")
        self._cleanup()

    def clear_handlers(self) -> None:
        """
        Removes all registered exit handlers.

        Note:
            Once all handlers are removed, the handler unregisters itself from the `atexit` module.

        Returns:
            None
        """
        log = self.method_logger

        log.debug("Clearing all exit handlers")
        self._handlers.clear()
        log.debug("All exit handlers cleared")

    def find_handler_by_uuid(self, uuid):
        log = self.method_logger

        if not isinstance(uuid, (UUID, str)):
            log.error("UUID must be a UUID object or a string")
            raise ValueError("UUID must be a UUID object or a string")

        if isinstance(uuid, str):
            uuid = UUID(uuid)

        for entry in self.handlers:
            if entry.get('uuid') and entry['uuid'] == uuid:
                return entry

    def function_registered(self, func):
        return any([entry['func'] == func for entry in self.handlers])

    def has_key(self, key):
        return key in self.handler_keys

    def has_uuid(self, uuid):
        return any([entry.get('uuid') == uuid for entry in self.handlers])

    def register_handler(self, func, *args, return_func=False, **kwargs):
        log = self.method_logger

        log.debug(f"Registering exit handler {func} | Args: {args} | Kwargs: {kwargs}")

        # Check if the function is already registered
        log.debug(f"Checking if handler {func} is already registered")

        # Create a unique key from the function, its args, and kwargs
        new_key = self._get_key(func, args, kwargs)

        log.debug(f"New key: {new_key}")

        if self.has_key(new_key):
            log.warning(f"Handler {func} is already registered")
            return func


        info = {
            'handler_info': {
                'module': func.__module__,
                'name': func.__name__,
            },
            'func': func,
            'args': args,
            'kwargs': kwargs,
            'uuid': uuid4()
        }

        with self._lock:
            # Otherwise, add the handler
            self.handlers.append(info)
            log.debug(f"Handler {func} registered successfully")

        return info['uuid']

    def register_self_with_atexit(self):
        log = self.method_logger

        log.debug('Checking if registered with atexit already...')

        if not self.registered_with_atexit:
            log.debug('Registering with atexit...')
            atexit.register(self._cleanup)
            self.__registered_with_atexit = True

    def unregister_all(self):
        self.clear_handlers()

    def unregister_all_with_name(self, name: str) -> None:
        """
        Unregister all exit handlers with a specific name.

        Parameters:
            name (str):
                The name of the exit handlers to unregister.

        Returns:
            None
        """
        log = self.method_logger

        log.debug(f"Unregistering all exit handlers with name {name}")

        for entry in self._handlers:
            if 'handler_info' in entry:
                info = entry['handler_info']
                if info.get('name') == name:
                    log.debug(f"Removing handler {info.get('module', '')}.{info.get('name')}")
                    self._handlers.remove(entry)

        log.debug(f"All handlers with name {name} unregistered successfully")

    def unregister_by_uuid(self, uuid):
        log = self.method_logger

        log.debug(f"Unregistering exit handler with UUID {uuid}")

        handler = self.find_handler_by_uuid(uuid)

        if handler:
            log.debug(f"Removing handler {handler['func']}")
            self._handlers.remove(handler)
            log.debug(f"Handler with UUID {uuid} unregistered successfully")
            return True

        log.warning(f"Handler with UUID {uuid} not found")

        return False

    def unregister_handler(self, func, *args, **kwargs):
        log = self.method_logger

        log.debug(f"Unregistering exit handler {func} | Args: {args} | Kwargs: {kwargs}")

        # Create a unique key from the function, its args, and kwargs
        key = (func, args, frozenset(kwargs.items()))

        log.debug(f"Key: {key}")

        for entry in self._handlers:
            existing_key = (entry['func'], entry['args'], frozenset(entry['kwargs'].items()))
            if existing_key == key:
                log.debug(f"Removing handler {func}")
                self._handlers.remove(entry)
                log.debug(f"Handler {func} unregistered successfully")
                return func

        log.warning(f"Handler {func} not found")
        return None

    def unregister_self_with_atexit(self):
        log = self.method_logger

        log.debug('Checking if registered with atexit already...')

        if self.registered_with_atexit:
            log.debug('Unregistering with atexit...')
            atexit.unregister(self._cleanup)
            self.__registered_with_atexit = False
            return True
        else:
            log.warning('ExitCallHandler is not registered with atexit!')

        return False

