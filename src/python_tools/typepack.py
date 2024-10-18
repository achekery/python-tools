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


# Below is a test case script for verifying these classes.
# Move the script into a separate file and run it from there.

_ = '''


import sys
import traceback

null, false, true = None, False, True

def test_common(inputs, checks, klass):
    print(f"test_common >>> {klass=}")
    obj = klass()
    for count, (name, ar, exp) in enumerate(zip(*inputs)):
        if name == klass.__name__.split("_")[0]:
            obj = klass(*ar)
            func = lambda *x, **y: (None, None)
        else:
            func = getattr(obj, name)
        check = [k for k, v in checks.items() if name in v][0]
        msg = f"when {name=}, {ar=}"
        try:
            res = func(*ar)
        except Exception as exc:
            msg += f" -> {exc=}"
            print(msg)
            traceback.print_exc()
            continue
        else:
            msg += f" -> {check=}: {res=}, {exp=}"
        match check:
            case "ignore":
                pass
            case "eq":
                assert res == exp, msg
            case "eq_when_sorted_two_deep":
                assert sorted([sorted(v) for v in res]) == sorted([sorted(v) for v in exp]), msg
            case "in_list":
                assert res in exp, msg
            case _:
                raise ValueError(f"unknown check: {check=}")
        print(f"test_common : {msg=}")
    print(f"test_common <<<")

inputs = [
    ["MyHashMap","put","put","get","get","put","get","remove","get"],
    [[],[1,1],[2,2],[1],[3],[2,1],[2],[2],[2]],
    [null,null,null,1,-1,null,1,null,-1],
]
checks = {
    "ignore": [
        "MyHashMap",
        "put",
        "remove"
    ],
    "eq": [
        "get"
    ],
    "eq_when_sorted_two_deep": [

    ],
    "in_list": [

    ],
}
for klass in [
    MyHashMap_MutableMapping,
    MyHashMap_Dict,
]:
    _ = test_common(inputs, checks, klass); print()

'''

# Below is a perf mapping script to characterize these classes.
# Move the script into a separate file and run it from there.

_ = '''
import random
import timeit

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

"""
Problem:
  Design Linked List

Design your implementation of the linked list. You can choose to use
a singly or doubly linked list. A node in a singly linked list should
have two attributes: val and next. val is the value of the current node,
and next is a pointer/reference to the next node. If you want to use the
doubly linked list, you will need one more attribute prev to indicate
the previous node in the linked list. Assume all nodes in the linked
list are 0-indexed.

Implement the MyLinkedList class:

* MyLinkedList() Initializes the MyLinkedList object.

* int get(int index) Get the value of the indexth node in the linked
list. If the index is invalid, return -1.

* void addAtHead(int val) Add a node of value val before the first
element of the linked list. After the insertion, the new node will be
the first node of the linked list.

* void addAtTail(int val) Append a node of value val as the last element
of the linked list.

* void addAtIndex(int index, int val) Add a node of value val before the
indexth node in the linked list. If index equals the length of the
linked list, the node will be appended to the end of the linked list. If
index is greater than the length, the node will not be inserted.

* void deleteAtIndex(int index) Delete the indexth node in the linked
list, if the index is valid.
"""

from abc import ABC, abstractmethod
from collections.abc import MutableSequence
from dataclasses import dataclass
from typing import Generator, Optional

class _LinkedList_MutableSequence(MutableSequence):

    @dataclass
    class _LinkedListValue():
        element: int

    @dataclass
    class _LinkedListNode():
        value: "_LinkedListValue"
        next: "_LinkedListNode" = None

    @dataclass
    class _LinkedList():
        head: "_LinkedListNode" = None

    def __init__(self) -> None:
        self._nodes = self.__class__._LinkedList()

    # Required for implementing the Sequence ABC.
    # See https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

    def _walk(self) -> Generator["_LinkedListNode", None, None]:
        node = self._nodes.head
        while node is not None:
            yield node
            node = node.next

    def __iter__(self) -> Generator["_LinkedListValue", None, None]:
        """This method is called when an iterator is required for a container."""
        for node in self._walk():
            yield node.value

    def __getitem__(self, key: int) -> "_LinkedListValue":
        """Called to implement evaluation of self[key]."""
        for count, node in enumerate(self._walk()):
            if count == key:
                return node.value
        raise IndexError(key)

    def __len__(self) -> int:
        """Called to implement the built-in function len()."""
        count = -1
        for count, node in enumerate(self._walk()):
            pass
        return count + 1

    # Required for implementing the MutableSequence ABC.
    # See https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes

    def __setitem__(self, key: int, value: "_LinkedListValue") -> None:
        """Called to implement assignment to self[key]."""
        for count, node in enumerate(self._walk()):
            if count == key:
                node.value = value
                return
        raise IndexError(key)

    def __delitem__(self, key: int) -> None:
        """Called to implement deletion of self[key]."""
        if key == 0:
            if self._nodes.head is not None:
                self._nodes.head = self._nodes.head.next
            else:
                self._nodes.head = None
            return
        for count, prev in enumerate(self._walk()):
            if count == (key - 1):
                if prev.next is not None:
                    prev.next = prev.next.next
                else:
                    prev.next = None
                return
        raise IndexError(key)

    def insert(self, key: int, value: "_LinkedListValue") -> None:
        """Insert an item at a given position."""
        inserted = self.__class__._LinkedListNode(value)
        if key == 0:
            if self._nodes.head is not None:
                inserted.next = self._nodes.head
                self._nodes.head = inserted
            else:
                self._nodes.head = inserted
            return
        for count, prev in enumerate(self._walk()):
            if count == (key - 1):
                if prev.next is not None:
                    inserted.next = prev.next
                    prev.next = inserted
                else:
                    prev.next = inserted
                return
        raise IndexError(key)


class LinkedListLeetCodeBase(ABC):

    @abstractmethod
    def get(self, index: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def addAtHead(self, val: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def addAtTail(self, val: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def addAtIndex(self, index: int, val: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def deleteAtIndex(self, index: int) -> None:
        raise NotImplementedError()


class LinkedListLeetCode_MutableSequence(LinkedListLeetCodeBase):
    """Implement a linked list using a mutable sequence.

    Submission on LeetCode:
        * Runtime 279 ms (Beats 5.03%)
        * Memory 18.11 MB (Beats 17.44%)
    """

    def __init__(self) -> None:
        self._linkedlist = _LinkedList_MutableSequence()

    def __str__(self) -> str:
        return str(list(iter(self._linkedlist)))

    # Required for implementing the LinkedListLeetCodeBase ABC.

    def get(self, index: int) -> int:
        try:
            return self._linkedlist[index].element
        except IndexError:
            return -1

    def addAtHead(self, value: int) -> None:
        self.addAtIndex(0, value)

    def addAtTail(self, value: int) -> None:
        self.addAtIndex(len(self._linkedlist), value)

    def addAtIndex(self, index: int, value: int) -> None:
        try:
            self._linkedlist.insert(index, _LinkedList_MutableSequence._LinkedListValue(value))
        except IndexError:
            return

    def deleteAtIndex(self, index: int) -> None:
        try:
            del self._linkedlist[index]
        except IndexError:
            return


from collections import deque

class LinkedListLeetCode_Deque(LinkedListLeetCodeBase):
    """Implement a linked list using a deque.

    Submission on LeetCode:
        * Runtime 11 ms (Beats 100.00%)
        * Memory 17.92 MB (Beats 32.28%)
    """

    def __init__(self) -> None:
        self._linkedlist = deque()

    def __str__(self) -> str:
        return str(list(iter(self._linkedlist)))

    # Required for implementing LinkedListLeetCodeBase ABC.

    def get(self, index: int) -> int:
        try:
            return self._linkedlist[index]
        except IndexError:
            return -1

    def addAtHead(self, val: int) -> None:
        self._linkedlist.appendleft(val)

    def addAtTail(self, val: int) -> None:
        self._linkedlist.append(val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index > len(self._linkedlist):
            return
        try:
            self._linkedlist.insert(index, val)
        except IndexError:
            return

    def deleteAtIndex(self, index: int) -> None:
        try:
            del self._linkedlist[index]
        except IndexError:
            return
