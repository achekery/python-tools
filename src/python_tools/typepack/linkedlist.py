#@title Doubly Linked List // Design Linked List

"""
Problem:
    Classic Problems // Design Linked List
    https://leetcode.com/explore/learn/card/linked-list/210/doubly-linked-list/1294/

Description:
    Design your implementation of the linked list. You can choose to use a
    singly or doubly linked list.

    A node in a singly linked list should have two attributes: val and next.
    val is the value of the current node, and next is a pointer/reference to
    the next node.

    If you want to use the doubly linked list, you will need one more
    attribute prev to indicate the previous node in the linked list. Assume
    all nodes in the linked list are 0-indexed.

Implement the MyLinkedList class:
    MyLinkedList() Initializes the MyLinkedList object.

    int get(int index) Get the value of the indexth node in the linked list.
    If the index is invalid, return -1.

    void addAtHead(int val) Add a node of value val before the first element
    of the linked list. After the insertion, the new node will be the first
    node of the linked list.

    void addAtTail(int val) Append a node of value val as the last element
    of the linked list.

    void addAtIndex(int index, int val) Add a node of value val before the
    indexth node in the linked list. If index equals the length of the
    linked list, the node will be appended to the end of the linked list. If
    index is greater than the length, the node will not be inserted.

    void deleteAtIndex(int index) Delete the indexth node in the linked
    list, if the index is valid.

Constraints:
    0 <= index, val <= 1000

    Please do not use the built-in LinkedList library.

    At most 2000 calls will be made to get, addAtHead, addAtTail, addAtIndex
    and deleteAtIndex.
"""

from abc import ABC, abstractmethod

class LeetCodeApi(ABC):

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


from collections import deque

class MyLinkedList_Deque_LeetCodeApi(LeetCodeApi):

    def __init__(self) -> None:
        self._linkedlist = deque()

    def __str__(self) -> str:
        return str(list(iter(self._linkedlist)))

    # Implements MyLinkedList_LeetCodeBase ABC

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

from collections.abc import MutableSequence
from dataclasses import dataclass
from typing import Generator, Optional

class _MyLinkedList_MutableSequence(MutableSequence):

    @dataclass
    class _LinkedListNode():
        value: int
        next: "_LinkedListNode" = None
        prev: "_LinkedListNode" = None

    @dataclass
    class _LinkedList():
        head: "_LinkedListNode" = None

    def __init__(self) -> None:
        self._nodes = self.__class__._LinkedList()

    # Implements Sequence
    def _walk(self) -> Generator["_LinkedListNode", None, None]:
        node = self._nodes.head
        while node is not None:
            yield node
            node = node.next

    def __iter__(self) -> Generator[int, None, None]:
        """This method is called when an iterator is required for a container."""
        for node in self._walk():
            yield node.value

    def __getitem__(self, key: int) -> int:
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

    # Implements MutableSequence
    def __setitem__(self, key: int, value: int) -> None:
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

    def insert(self, key: int, value: int) -> None:
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

class MyLinkedList_MutableSequence_LeetCodeApi(LeetCodeApi):

    def __init__(self) -> None:
        self._linkedlist = _MyLinkedList_MutableSequence()

    def __str__(self) -> str:
        return str(list(iter(self._linkedlist)))

    # Implements LeetCodeApi
    def get(self, index: int) -> int:
        try:
            return self._linkedlist[index]
        except IndexError:
            return -1

    def addAtHead(self, value: int) -> None:
        self.addAtIndex(0, value)

    def addAtTail(self, value: int) -> None:
        self.addAtIndex(len(self._linkedlist), value)

    def addAtIndex(self, index: int, value: int) -> None:
        try:
            self._linkedlist.insert(index, value)
        except IndexError:
            return

    def deleteAtIndex(self, index: int) -> None:
        try:
            del self._linkedlist[index]
        except IndexError:
            return


class MyLinkedList_Simple_LeetCodeApi(LeetCodeApi):

    @dataclass
    class _LinkedListNode():
        value: int
        next: "_LinkedListNode" = None
        prev: "_LinkedListNode" = None

    @dataclass
    class _LinkedList():
        head: "_LinkedListNode" = None
        tail: "_LinkedListNode" = None
        length: int = 0

        def __str__(self) -> str:
            ptr = self.head; msg = "LinkedList: "
            while ptr is not None:
                msg += f"<-({ptr.value})->"
                ptr = ptr.next
            return msg

    def __init__(self) -> None:
        self._linkedlist = self.__class__._LinkedList()

    def __str__(self) -> str:
        return str(list(iter(self._linkedlist)))

    # Implements LeetCodeApi
    def _walk(self, index: int) -> "_LinkedListNode":
        ptr = self._linkedlist.head; cnt = 0
        while ptr is not None:
            if cnt == index:
                return ptr
            ptr = ptr.next; cnt += 1
        raise IndexError(index)

    def get(self, index: int) -> int:
        try:
            ptr = self._walk(index)
        except IndexError:
            return -1
        return ptr.value

    def addAtHead(self, value: int) -> None:
        self.addAtIndex(0, value)

    def addAtTail(self, value: int) -> None:
        self.addAtIndex(self._linkedlist.length, value)

    def _insertAtIndex(self, index: int, value: int) -> None:
        inserted = self.__class__._LinkedListNode(value)
        if self._linkedlist.length == 0 and index == 0:
            # add to empty list
            self._linkedlist.head = self._linkedlist.tail = inserted
        elif index == 0:
            # push to the front
            inserted.next = self._linkedlist.head; self._linkedlist.head.prev = inserted
            self._linkedlist.head = inserted
        elif index == self._linkedlist.length:
            # push to the back
            self._linkedlist.tail.next = inserted; inserted.prev = self._linkedlist.tail
            self._linkedlist.tail = inserted
        else:
            # insert in the middle
            ptr_previous = self._walk(index - 1)  # raises IndexError
            inserted.next = ptr_previous.next; ptr_previous.next.prev = inserted
            ptr_previous.next = inserted; inserted.prev = ptr_previous
        self._linkedlist.length += 1

    def addAtIndex(self, index: int, value: int) -> None:
        try:
            self._insertAtIndex(index, value)
        except IndexError:
            return

    def _removeAtIndex(self, index: int) -> None:
        if self._linkedlist.length == 0:
            # ignore empty list
            return
        if index == 0:
            # pop from the front
            if self._linkedlist.head.next is not None:
                self._linkedlist.head.next.prev = None
            self._linkedlist.head = self._linkedlist.head.next
        elif index == self._linkedlist.length - 1:
            # pop from the back
            if self._linkedlist.tail.prev is not None:
                self._linkedlist.tail.prev.next = None
            self._linkedlist.tail = self._linkedlist.tail.prev
        else:
            # remove in the middle
            ptr_removed = self._walk(index)  # raises IndexError
            if ptr_removed.next is not None:
                ptr_removed.next.prev = ptr_removed.prev
            ptr_removed.prev.next = ptr_removed.next
        self._linkedlist.length -= 1

    def deleteAtIndex(self, index: int) -> None:
        try:
            self._removeAtIndex(index)
        except IndexError:
            return

# # if __name__ == "__main__":
# #     import sys
# #     if "IPython" not in sys.modules:
# #         MyLinkedList = MyLinkedList_Simple_LeetCodeApi
# #     else:
# #         null = None; false = False; true = True
# #         klasses = [
# #             MyLinkedList_Deque_LeetCodeApi,
# #             MyLinkedList_MutableSequence_LeetCodeApi,
# #             MyLinkedList_Simple_LeetCodeApi,
# #         ]
# #         input = [
# #             ["MyLinkedList","addAtHead","deleteAtIndex","addAtHead","addAtHead","addAtHead","addAtHead","addAtHead","addAtTail","get","deleteAtIndex","deleteAtIndex"],
# #             [[],[2],[1],[2],[7],[3],[2],[5],[5],[5],[6],[4]],
# #         ]
# #         output = [
# #             [null,null,null,null,null,null,null,null,null,2,null,null]
# #         ]
# #         # input = [
# #         #     ["MyLinkedList", "addAtHead", "deleteAtIndex"],
# #         #     [[], [1], [0]],
# #         # ]
# #         # output = [
# #         #     [null, null, null]
# #         # ]
# #         # input = [
# #         #     ["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"],
# #         #     [[], [1], [3], [1, 2], [1], [1], [1]],
# #         # ]
# #         # output = [
# #         #     [null, null, null, null, 2, null, 3]
# #         # ]
# #         obj = None
# #         for klass in klasses:
# #             print(); print(f"loop >>> {klass.__name__=}")
# #             for name, args, exp in zip(*input, *output):
# #                 print(); print(f"{name=} {args=} {exp=}")
# #                 if name == "MyLinkedList":
# #                     obj = klass(*args)
# #                 else:
# #                     res = getattr(obj, name)(*args)
# #                     print(f"{str(obj._linkedlist)=}")
# #                     assert res == exp, f"{res=!s} != {exp=!s}"
# #             print(f"loop <<< {klass.__name__=}")

# #         print(); print("done!")