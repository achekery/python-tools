"""
Problem:
    Design HashMap

Objective:
    Design a HashMap without using any built-in hash table libraries.

Task:
    Implement the MyHashMap class:

    * MyHashMap() initializes the object with an empty map.

    * void put(int key, int value) inserts a (key, value) pair into the
      HashMap. If the key already exists in the map, update the
      corresponding value.

    * int get(int key) returns the value to which the specified key is
      mapped, or -1 if this map contains no mapping for the key.

    * void remove(key) removes the key and its corresponding value if the
      map contains the mapping for the key.

Constraints

    * 0 <= key, value <= 10 ** 6
    * At most 10 ** 4 calls will be made to put, get, and remove.
"""



# ======================================================================
# Part 1: Designs for deque bucket type and mutable mapping.
# ======================================================================

import copy
from collections import deque
from collections.abc import MutableMapping
from dataclasses import dataclass
from typing import Generator
try:
    from typing_extensions import Self
except ImportError:
    from typing import Self


class _MyHashMap_MutableMapping(MutableMapping):

    @dataclass
    class MyBucketNode():
        key: int
        value: int

        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return self.key == other.key
            if isinstance(other, int):
                return self.key == other
            return False

    @dataclass
    class MyBucket():
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
        except ValueError as exc:
            nodes.appendleft(self.__class__.MyBucketNode(key, value))
        else:
            nodes[i].value = value

    def __delitem__(self, key: int) -> None:
        nodes = self._buckets_resolve(key).nodes
        try:
            i = nodes.index(key)
        except ValueError as exc:
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


class MyHashMap_MutableMapping():

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


class MyHashMap_Dict():

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


# ======================================================================
# Part 2: Designs for multiple bucket types (deque, list, linkedlist).
# ======================================================================

from abc import ABC, abstractmethod

class LeetCodeApi(ABC):

    @abstractmethod
    def put(self, key: int, value: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, key: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def remove(self, key: int) -> None:
        raise NotImplementedError()

from dataclasses import dataclass
from typing import List, Tuple, Optional, Any

from collections import deque
from typing import Deque

class MyHashMap_DequeBuckets_LeetCode(LeetCodeApi):
    # Submission 10/25: Runtime 97 ms (94 pct), Memory 21.35 MB (23 pct)

    @dataclass
    class _HashMapItem():
        key: int
        value: int

    def __init__(self) -> None:
        self._hashmap_buckets = [deque() for _ in range(1024)]

    # HashMap Utilities
    def _hashmap_hashcode(self, key: int) -> int:
        return key % len(self._hashmap_buckets)

    def _hashmap_hashbucket(self, key: int) -> Deque["_HashMapItem"]:
        return self._hashmap_buckets[self._hashmap_hashcode(key)]

    def _hashmap_find(self, key: int) -> "_HashMapItem":
        for item in self._hashmap_hashbucket(key):
            if item.key == key:
                return item
        raise IndexError(f"Missing key in buckets: {key=}")

    # Implements LeetCodeApi
    def put(self, key: int, value: int) -> None:
        try:
            self._hashmap_find(key).value = value
        except IndexError:
            item = self.__class__._HashMapItem(key, value)
            self._hashmap_hashbucket(key).appendleft(item)

    def get(self, key: int) -> int:
        try:
            return self._hashmap_find(key).value
        except IndexError:
            return -1

    def remove(self, key: int) -> None:
        try:
            item = self._hashmap_find(key)
            self._hashmap_hashbucket(key).remove(item)
        except IndexError:
            pass

class MyHashMap_ListBuckets_LeetCode(LeetCodeApi):
    # Submission 10/25: Runtime 89 ms (94 pct), Memory 20.3 MB (31 pct)

    @dataclass
    class _HashMapItem():
        key: int
        value: int

    def __init__(self) -> None:
        self._hashmap_buckets = [list() for _ in range(1024)]

    # HashMap Utilities
    def _hashmap_hashcode(self, key: int) -> int:
        return key % len(self._hashmap_buckets)

    def _hashmap_findbucket(self, key: int) -> List["_HashMapItem"]:
        return self._hashmap_buckets[self._hashmap_hashcode(key)]

    def _hashmap_finditem(self, key: int) -> Tuple["_HashMapItem", int]:
        for index, item in enumerate(self._hashmap_findbucket(key)):
            if item.key == key:
                return item, index
        raise IndexError(f"Missing key in buckets: {key=}")

    # Implements LeetCodeApi
    def put(self, key: int, value: int) -> None:
        try:
            item, _ = self._hashmap_finditem(key)
            item.value = value
        except IndexError:
            item = self.__class__._HashMapItem(key, value)
            self._hashmap_findbucket(key).insert(0, item)

    def get(self, key: int) -> int:
        try:
            item, _ = self._hashmap_finditem(key)
            return item.value
        except IndexError:
            return -1

    def remove(self, key: int) -> None:
        try:
            _, index = self._hashmap_finditem(key)
            bucket = self._hashmap_findbucket(key)
            bucket[index] = bucket[0]; _ = bucket.pop(0)
        except IndexError:
            pass

class MyHashMap_SimpleLinkedListBuckets_LeetCode(LeetCodeApi):
    # Submission 10/25: Runtime 107 ms (94 pct), Memory 20.5 MB (27 pct)

    @dataclass
    class _HashMapItem():
        key: int
        value: int

    class _SimpleLinkedListNode():
        def __init__(self, item: "_HashMapItem") -> None:
            self.item: "_HashMapItem" = item
            self.next: Optional["_SimpleLinkedListNode"] = None

    class _SimpleLinkedList():
        def __init__(self) -> None:
            self.head: Optional["_SimpleLinkedListNode"] = None

    def __init__(self) -> None:
        self._hashmap_buckets = [self.__class__._SimpleLinkedList() for _ in range(1024)]

    # HashMap Utilities
    def _hashmap_hashcode(self, key: int) -> int:
        return key % len(self._hashmap_buckets)

    def _hashmap_findbucket(self, key: int) -> "_SimpleLinkedList":
        return self._hashmap_buckets[self._hashmap_hashcode(key)]

    def _hashmap_finditem_bykey(self, key: int) -> Tuple["_SimpleLinkedListNode", int]:
        item = self._hashmap_findbucket(key).head; cnt = 0
        while item is not None:
            if item.item.key == key:
                return item, cnt
            item = item.next; cnt += 1
        raise IndexError(f"Missing key in buckets: {key=}")

    def _hashmap_finditem_byindex(self, key: int, index: int) -> "_SimpleLinkedListNode":
        item = self._hashmap_findbucket(key).head; cnt = 0
        while item is not None:
            if cnt == index:
                return item
            item = item.next; cnt += 1
        raise ValueError(f"Index not in buckets: {index=}")

    # Implements LeetCodeApi
    def put(self, key: int, value: int) -> None:
        try:
            node, _ = self._hashmap_finditem_bykey(key)
            node.item.value = value
        except IndexError:
            node = self.__class__._SimpleLinkedListNode(self.__class__._HashMapItem(key, value))
            bucket = self._hashmap_findbucket(key)
            node.next = bucket.head; bucket.head = node  # insert to head

    def get(self, key: int) -> int:
        try:
            node, _ = self._hashmap_finditem_bykey(key)
            return node.item.value
        except IndexError:
            return -1

    def remove(self, key: int) -> None:
        try:
            node, index = self._hashmap_finditem_bykey(key)
            bucket = self._hashmap_findbucket(key)
            if node != bucket.head:  # move to head
                prev = self._hashmap_finditem_byindex(key, index - 1)
                prev.next = prev.next.next
                node.next = bucket.head; bucket.head = node
            bucket.head = bucket.head.next  # remove from head
        except IndexError:
            pass



# # # ------------------------------------------------------------------------------

# # import random
# # import sys
# # import timeit

# # if __name__ == "__main__" and False:
# #     if "google.colab" in sys.modules:
# #         def perf_mapping(klass, repeat=100):
# #             print(f"perf_mapping >>> {klass=}, {repeat=}")
# #             timer = timeit.Timer(
# #                 stmt='_ = [m.put(random.randint(0, 10 ** 6), random.randint(0, 10 ** 6)) for _ in range(10 ** 4)]',
# #                 setup=f"m=MyHashMap()",
# #                 globals={"random": random, "MyHashMap": klass},
# #             )
# #             number, time_taken = timer.autorange()
# #             autorange_stats = {
# #                 "number": number,
# #                 "time_taken": time_taken,
# #             }
# #             print(f"{autorange_stats=}")
# #             results = timer.repeat(repeat=repeat, number=number)
# #             repeat_stats = {
# #                 "len": len(results),
# #                 "min": min(results),
# #                 "max": max(results),
# #                 "avg": sum(results) / len(results),
# #             }
# #             print(f"{repeat_stats=}")
# #             perf_time = repeat_stats["min"]
# #             print(f"perf_mapping <<< {perf_time=}")
# #             return perf_time

# #         for klass in [
# #             MyHashMap_MutableMapping,
# #             MyHashMap_Dict,
# #         ]:
# #             _ = perf_mapping(klass, repeat=100); print()

# # _ = """
# # perf_mapping >>> klass=<class '__main__.MyHashMap_MutableMapping'>, repeat=100
# # autorange_stats={'number': 2, 'time_taken': 0.20886899599918252}
# # repeat_stats={'len': 100, 'min': 0.16895363000003272, 'max': 0.7509531209998386, 'avg': 0.22262870485003985}
# # perf_mapping <<< perf_time=0.16895363000003272

# # perf_mapping >>> klass=<class '__main__.MyHashMap_Dict'>, repeat=100
# # autorange_stats={'number': 5, 'time_taken': 0.2182407489999605}
# # repeat_stats={'len': 100, 'min': 0.10220586800005549, 'max': 0.23207494700000098, 'avg': 0.12748984417001338}
# # perf_mapping <<< perf_time=0.10220586800005549
# # """

# # # ------------------------------------------------------------------------------

# # import sys
# # import traceback

# # if __name__ == "__main__":
# #     if "google.colab" in sys.modules:
# #         null, false, true = None, False, True

# #         def test_common(inputs, checks, klass):
# #             print(f"test_common >>> {klass=}")
# #             obj = klass()
# #             for count, (name, ar, exp) in enumerate(zip(*inputs)):
# #                 if name == klass.__name__.split("_")[0]:
# #                     obj = klass(*ar)
# #                     func = lambda *x, **y: (None, None)
# #                 else:
# #                     func = getattr(obj, name)
# #                 check = [k for k, v in checks.items() if name in v][0]
# #                 msg = f"when {name=}, {ar=}"
# #                 try:
# #                     res = func(*ar)
# #                 except Exception as exc:
# #                     msg += f" -> {exc=}"
# #                     print(msg)
# #                     traceback.print_exc()
# #                     continue
# #                 else:
# #                     msg += f" -> {check=}: {res=}, {exp=}"
# #                 match check:
# #                     case "ignore":
# #                         pass
# #                     case "eq":
# #                         assert res == exp, msg
# #                     case "eq_when_sorted_two_deep":
# #                         assert sorted([sorted(v) for v in res]) == sorted([sorted(v) for v in exp]), msg
# #                     case "in_list":
# #                         assert res in exp, msg
# #                     case _:
# #                         raise ValueError(f"unknown check: {check=}")
# #                 print(f"test_common : {msg=}")
# #             print(f"test_common <<<")

# #         inputs = [
# #             ["MyHashMap","put","put","get","get","put","get","remove","get"],
# #             [[],[1,1],[2,2],[1],[3],[2,1],[2],[2],[2]],
# #             [null,null,null,1,-1,null,1,null,-1],
# #         ]
# #         checks = {
# #             "ignore": [
# #                 "MyHashMap",
# #                 "put",
# #                 "remove"
# #             ],
# #             "eq": [
# #                 "get"
# #             ],
# #             "eq_when_sorted_two_deep": [

# #             ],
# #             "in_list": [

# #             ],
# #         }
# #         for klass in [
# #             # MyHashMap_MutableMapping,
# #             # MyHashMap_Dict,
# #             MyHashMap_DequeBuckets_LeetCode,
# #             MyHashMap_ListBuckets_LeetCode,
# #             MyHashMap_SimpleLinkedListBuckets_LeetCode,
# #         ]:
# #             _ = test_common(inputs, checks, klass); print()

# # _ = """

# # test_common >>> klass=<class '__main__.MyHashMap_MutableMapping'>
# # test_common : msg="when name='MyHashMap', ar=[] -> check='ignore': res=(None, None), exp=None"
# # test_common : msg="when name='put', ar=[1, 1] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='put', ar=[2, 2] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[1] -> check='eq': res=1, exp=1"
# # test_common : msg="when name='get', ar=[3] -> check='eq': res=-1, exp=-1"
# # test_common : msg="when name='put', ar=[2, 1] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[2] -> check='eq': res=1, exp=1"
# # test_common : msg="when name='remove', ar=[2] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[2] -> check='eq': res=-1, exp=-1"
# # test_common <<<

# # test_common >>> klass=<class '__main__.MyHashMap_Dict'>
# # test_common : msg="when name='MyHashMap', ar=[] -> check='ignore': res=(None, None), exp=None"
# # test_common : msg="when name='put', ar=[1, 1] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='put', ar=[2, 2] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[1] -> check='eq': res=1, exp=1"
# # test_common : msg="when name='get', ar=[3] -> check='eq': res=-1, exp=-1"
# # test_common : msg="when name='put', ar=[2, 1] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[2] -> check='eq': res=1, exp=1"
# # test_common : msg="when name='remove', ar=[2] -> check='ignore': res=None, exp=None"
# # test_common : msg="when name='get', ar=[2] -> check='eq': res=-1, exp=-1"
# # test_common <<<

# # """
