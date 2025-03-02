from collections import UserList
from typing import Optional


class HandlerList(UserList):
    """
    A list-like object that triggers a callback when the list either becomes empty or non-empty.
    """
    def __init__(self, *args, on_empty=None, on_non_empty=None):
        super().__init__(*args)
        self.__on_empty = on_empty if callable(on_empty) else None
        self.__on_non_empty = on_non_empty if callable(on_non_empty) else None
        self.__was_empty = not bool(self.data)

    def _check_state(self) -> None:
        """
        Check the current state of the list and trigger the appropriate callback.

        Returns:
             None
        """
        is_empty = not bool(self.data)

        if is_empty and not self.was_empty:
            self.on_empty()
        elif not is_empty and self.was_empty:
            self.on_non_empty()

        self.__was_empty = is_empty

    @property
    def on_empty(self) -> Optional[callable]:
        return self.__on_empty

    @property
    def on_non_empty(self) -> Optional[callable]:
        return self.__on_non_empty

    @property
    def was_empty(self) -> bool:
        return self.__was_empty

    def append(self, item) -> None:
        """
        Append an item to the list and check the state.

        Parameters:
            item:
                The item to be appended.

        Returns:
            None
        """
        super().append(item)
        self._check_state()

    def clear(self) -> None:
        """
        Clear the list and check the state.

        Returns:
            None
        """
        super().clear()
        self._check_state()

    def extend(self, other: list) -> None:
        """
        Extend the list with another iterable and check the state.

        Parameters:
            other:
                The iterable to extend the list with.

        Returns:
            None
        """
        super().extend(other)
        self._check_state()

    def insert(self, index: int, item: any) -> None:
        """
        Insert an item at the specified index and check the state.

        Parameters:
            index (int):
                The index at which to insert the item.
            item (any):
                The item to be inserted.

        Returns:
            None
        """
        super().insert(index, item)
        self._check_state()

    def pop(self, index: int = -1) -> any:
        """
        Remove and return the item at the specified index and check the state.

        Parameters:
            index (int, optional):
                The index of the item to be removed. Defaults to the last item.
        """
        item = super().pop(index)
        self._check_state()

        return item

    def remove(self, item: any) -> None:
        """
        Remove the first occurrence of the specified item and check the state.

        Parameters:
            item (any):
                The item to be removed.

        Returns:
            None
        """
        super().remove(item)
        self._check_state()

