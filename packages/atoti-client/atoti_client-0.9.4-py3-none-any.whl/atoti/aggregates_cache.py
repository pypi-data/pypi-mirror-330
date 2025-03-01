from collections.abc import Callable
from typing import Final, final

from typing_extensions import override


@final
class AggregatesCache:
    """The aggregates cache associated with a :class:`~atoti.Cube`."""

    def __init__(
        self,
        *,
        set_capacity: Callable[[int], None],
        get_capacity: Callable[[], int],
    ) -> None:
        self._set_capacity: Final = set_capacity
        self._get_capacity: Final = get_capacity

    """Capacity of the cache.

    :meta private:

        If:

        * ``> 0``: corresponds to the maximum amount of ``{location: measure}`` pairs that the cache can hold.
        * ``0``: Sharing is enabled but caching is disabled.
          Queries will share their computations if they are executed at the same time, but the aggregated values will not be stored to be retrieved later.
        * ``< 0``: Caching and sharing are disabled.

        Example:
            .. doctest::
                :hide:

                >>> session = getfixture("default_session")

            >>> table = session.create_table("Example", data_types={"id": "int"})
            >>> cube = session.create_cube(table)
            >>> cube.aggregates_cache.capacity
            100
            >>> cube.aggregates_cache.capacity = -1
            >>> cube.aggregates_cache.capacity
            -1
        """

    @property
    def capacity(self) -> int:
        return self._get_capacity()

    @capacity.setter
    def capacity(self, capacity: int) -> None:
        self._set_capacity(capacity)

    @override
    def __repr__(self) -> str:
        return repr({"capacity": self.capacity})
