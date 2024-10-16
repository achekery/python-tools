"""typepack.py"""

import copy
from collections import deque
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Generator

try:
    from typing_extensions import Self
except ImportError:
    from typing import Self
else:
    Self = None  # pylint: disable=C0103:invalid-name



class _MyHashMap_MutableMapping(MutableMapping):

    @dataclass
    class MyBucketNode:
        key: int
        value: int

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.key == other.key
            if isinstance(other, int):
                return self.key == other
            return False

    @dataclass
    class MyBucket:
        nodes: deque

    def __init__(self, capacity=1024, other=None) -> None:
        if isinstance(other, self.__class__):
            self._buckets = copy.copy(other._buckets)
        else:
            self._buckets = [self.__class__.MyBucket(deque()) for _ in range(capacity)]

    def __str__(self) -> str:
        return str(dict(self.items()))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({vars(self)})"

    def _buckets_index(self, key: int) -> int:
        return key % len(self._buckets)

    def _buckets_resolve(self, key: int) -> "MyBucket":
        return self._buckets[self._buckets_index(key)]

    # Required for implementing the Mapping abstract base class.
    # See https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

    def __getitem__(self, key: int) -> int:
        nodes = self._buckets_resolve(key).nodes
        try:
            i = nodes.index(key)
        except ValueError as exc:
            raise KeyError(f"Missing key in nodes: {key=}") from exc
        else:
            return nodes[i].value

    def __iter__(self) -> Generator[int, None, None]:
        for bucket in self._buckets:
            for node in bucket.nodes:
                yield node.key

    def __len__(self) -> int:
        return len(self.keys())

    # Required for implementing the MutableMapping abstract base class.
    # See https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

    def __setitem__(self, key: int, value: int) -> None:
        nodes = self._buckets_resolve(key).nodes
        try:
            i = nodes.index(key)
        except ValueError:
            nodes.appendleft(self.__class__.MyBucketNode(key, value))
        else:
            nodes[i].value = value

    def __delitem__(self, key: int) -> None:
        nodes = self._buckets_resolve(key).nodes
        try:
            i = nodes.index(key)
        except ValueError:
            return
        else:
            nodes[i] = nodes[0]
            nodes.popleft()

    # Recommended for parity with the dict standard type.
    # See https://docs.python.org/3/reference/datamodel.html#emulating-container-types

    def copy(self) -> Self:
        return self.__class__(other=self)

    # Recommended for efficient use of the in operator.
    # See https://docs.python.org/3/reference/datamodel.html#emulating-container-types

    def __contains__(self, item) -> bool:
        for key in self.keys():
            if key == item:
                return True
        return False


class MyHashMap_MutableMapping:

    def __init__(self):
        self._hashmap = _MyHashMap_MutableMapping()

    def put(self, key: int, value: int) -> None:
        self._hashmap[key] = value

    def get(self, key: int) -> int:
        try:
            return self._hashmap[key]
        except KeyError:
            return -1

    def remove(self, key: int) -> None:
        del self._hashmap[key]


class MyHashMap_Dict:

    def __init__(self):
        self._hashmap = {}

    def put(self, key: int, value: int) -> None:
        self._hashmap[key] = value

    def get(self, key: int) -> int:
        try:
            return self._hashmap[key]
        except KeyError:
            return -1

    def remove(self, key: int) -> None:
        del self._hashmap[key]


# Below is a perf mapping script to characterize these classes.
# Move the script into a separate file and run it from there.

_ = '''
import random
import sys
import timeit

if __name__ == "__main__":
    if "google.colab" in sys.modules:
        def perf_mapping(klass, repeat=100):
            print(f"perf_mapping >>> {klass=}, {repeat=}")
            timer = timeit.Timer(
                stmt='_ = [m.put(random.randint(0, 10 ** 6), random.randint(0, 10 ** 6)) for _ in range(10 ** 4)]',
                setup=f"m=MyHashMap()",
                globals={"random": random, "MyHashMap": klass},
            )
            number, time_taken = timer.autorange()
            autorange_stats = {
                "number": number,
                "time_taken": time_taken,
            }
            print(f"{autorange_stats=}")
            results = timer.repeat(repeat=repeat, number=number)
            repeat_stats = {
                "len": len(results),
                "min": min(results),
                "max": max(results),
                "avg": sum(results) / len(results),
            }
            print(f"{repeat_stats=}")
            perf_time = repeat_stats["min"]
            print(f"perf_mapping <<< {perf_time=}")
            return perf_time

        for klass in [
            MyHashMap_MutableMapping,
            MyHashMap_Dict,
        ]:
            _ = perf_mapping(klass, repeat=100); print()
'''
