from dataclasses import dataclass
from typing import Optional as Opt, Generic, TypeVar, Union

T = TypeVar('T')


@dataclass
class DLNode(Generic[T]):
    val: T
    next: Opt['DLNode'] = None
    prev: Opt['DLNode'] = None

    def extract_from_list(self):
        prev, next = self.prev, self.next

        self.prev, self.next = None, None

        if prev is not None:
            prev.next = next
        if next is not None:
            next.prev = prev

    def __repr__(self) -> str:
        return f'val: {self.val},  next: {type(self.next)}, prev: {type(self.prev)}'


class DLList(Generic[T]):
    def __init__(self, arg: Union[DLNode, T]) -> None:
        if isinstance(arg, DLNode):
            if arg.next is not None or arg.prev is not None:
                raise ValueError()

            node = arg
        else:
            node = DLNode(arg)

        self.head: Opt[DLNode] = node
        self.tail: Opt[DLNode] = node
        self.length = 1

    def __len__(self) -> int:
        return self.length

    def __iter__(self) -> 'DLListIterator':
        return DLListIterator(self)

    def iter_over_nodes(self) -> 'DLListIterator':
        return DLListIterator(self, True)

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

        self.length += 1

    def pop(self) -> T:
        if self.tail is None:
            raise Exception('Nothing to pop')

        popped = self.tail
        self.tail = popped.prev
        popped.extract_from_list()

        if self.tail is None:
            self.head = None

        self.length -= 1

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

        self.length += 1

    def unshift(self) -> T:
        if self.head is None:
            raise Exception('Nothing to unshift')

        unshifted = self.head
        self.head = unshifted.next
        unshifted.extract_from_list()

        if self.head is None:
            self.tail = None

        self.length -= 1

        return unshifted.val

    def insert(self, val: T, before_node: DLNode = None, after_node: DLNode = None):
        if before_node is None and after_node is None:
            raise ValueError("Before or after node required")

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

            self.length += 1


class DLListIterator:
    def __init__(self, dllist: DLList[T], is_return_node: bool = False) -> None:
        self.dllist = dllist
        self.current = dllist.head
        self.is_return_node = is_return_node

    def __iter__(self) -> 'DLListIterator':
        return self

    def __next__(self) -> T:
        if self.current is None:
            raise StopIteration()

        r = self.current
        self.current = self.current.next

        return r if self.is_return_node else r.val
