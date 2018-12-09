from dataclasses import dataclass
from typing import Optional as Opt, Generic, TypeVar, Union, Generator
from collections.abc import Collection

T = TypeVar("T")


@dataclass
class DLNode(Generic[T]):
    val: T
    next: Opt["DLNode"] = None
    prev: Opt["DLNode"] = None

    def __repr__(self) -> str:
        return f"val: {self.val},  next: {type(self.next)}, prev: {type(self.prev)}"

    def extract_from_list(self) -> None:
        prev, next_ = self.prev, self.next

        self.prev, self.next = None, None

        if prev is not None:
            prev.next = next_
        if next_ is not None:
            next_.prev = prev


class DLList(Collection, Generic[T]):
    def __init__(self, arg: Union[DLNode, T]) -> None:
        if isinstance(arg, DLNode):
            if arg.next is not None or arg.prev is not None:
                raise ValueError()

            node = arg
        else:
            node = DLNode(arg)

        self.head: Opt[DLNode] = node
        self.tail: Opt[DLNode] = node
        self.__length = 1

    def __len__(self) -> int:
        return self.__length

    def __contains__(self, item: T) -> bool:
        cur = self.head
        for _ in range(self.__length):
            if cur.val == item:
                return True
            cur = cur.next

        return False

    def __iter__(self) -> Generator:
        cur = self.head
        for _ in range(self.__length):
            yield cur.val
            cur = cur.next

    def iter_over_nodes(self) -> Generator:
        cur = self.head
        for _ in range(self.__length):
            yield cur
            cur = cur.next

    def push(self, val: T) -> None:
        node = DLNode(val)

        tail = self.tail
        if tail is not None:
            tail.next = node
            node.prev = tail
            self.tail = node
        else:
            self.tail = node
            self.head = node

        self.__length += 1

    def pop(self) -> T:
        if self.tail is None:
            raise Exception("Nothing to pop")

        popped = self.tail
        self.tail = popped.prev
        popped.extract_from_list()

        if self.tail is None:
            self.head = None

        self.__length -= 1

        return popped.val

    def shift(self, val: T) -> None:
        node = DLNode(val)

        head = self.head
        if head is not None:
            head.prev = node
            node.next = head
            self.head = node
        else:
            self.head = node
            self.tail = node

        self.__length += 1

    def unshift(self) -> T:
        if self.head is None:
            raise Exception("Nothing to unshift")

        unshifted = self.head
        self.head = unshifted.next
        unshifted.extract_from_list()

        if self.head is None:
            self.tail = None

        self.__length -= 1

        return unshifted.val

    def insert(self, val: T, before_node: DLNode = None, after_node: DLNode = None) -> None:
        if before_node is None and after_node is None:
            raise ValueError("Before xor after node required")
        if before_node is not None and after_node is not None:
            raise ValueError("Before xor after node required, but XOR.")

        if before_node is self.head:
            return self.shift(val)
        elif after_node is self.tail:
            return self.push(val)
        else:
            node = DLNode(val)
            if before_node is not None:
                node.next = before_node
                node.prev = before_node.prev

                before_node.prev.next = node

                before_node.prev = node
            else:
                node.prev = after_node
                node.next = after_node.next

                after_node.next.prev = node

                after_node.next = node

            self.__length += 1

