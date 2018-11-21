from typing import List

import pytest

from endpoint.modules.structs import DLNode, DLListIterator, DLList


def _assert_order_and_values(dll: DLList, l: List) -> None:
    current = dll.head
    i = 0
    while current is not None:  # prime oreder
        assert current.val == l[i]

        current = current.next
        i += 1

    current = dll.tail
    i -= 1
    while current is not None:  # reverse oreder
        assert current.val == l[i]

        current = current.prev
        i -= 1


class TestDLNode:
    def test_dlnode_init(self):
        node = DLNode(13)
        assert node.val == 13
        assert node.next is None
        assert node.prev is None

        node2 = DLNode(12, node)
        assert node2.next is node

        node_next = DLNode(14)
        node_prev = DLNode(14)
        node3 = DLNode(14, node_next, node_prev)
        assert node3.next is node_next
        assert node3.prev is node_prev

    def test_dlnode_extract(self):
        node_next = DLNode(14)
        node_prev = DLNode(14)
        node3 = DLNode(14, node_next, node_prev)

        node3.extract_from_list()
        assert node_next.prev is node_prev
        assert node_next.next is None
        assert node_prev.prev is None
        assert node_prev.next is node_next


class TestDLList:
    def test_dllist_init(self):
        with pytest.raises(TypeError):
            DLList()

    def test_dllist_pop(self):
        ll = DLList(12)
        assert ll.pop() == 12
        with pytest.raises(Exception):
            ll.pop()

    def test_dllist_unshift(self):
        ll = DLList("k")
        assert ll.unshift() == "k"
        with pytest.raises(Exception):
            ll.unshift()

    def test_dllist_len(self):
        ll = DLList((1, 2))
        assert len(ll) == 1
        ll.shift((2, 3))
        assert len(ll) == 2
        ll.push((3, 4))
        assert len(ll) == 3

        ll.pop()
        assert len(ll) == 2
        ll.unshift()
        assert len(ll) == 1
        ll.pop()
        assert len(ll) == 0

    def test_dllist_complicated_case(self):
        ll3 = DLList(13)
        ll3.push(14)
        ll3.shift(12)
        ll3.push(15)
        assert ll3.unshift() == 12
        assert ll3.pop() == 15
        assert ll3.unshift() == 13
        assert ll3.pop() == 14

        with pytest.raises(Exception):
            ll3.pop()

    def test_dllist_iter(self):
        ll3 = DLList(13)
        iter_ll3 = iter(ll3)
        assert isinstance(iter_ll3, DLListIterator)
        assert iter_ll3.dllist is ll3
        assert iter_ll3.current is ll3.head

    def test_dllist_insert_exception(self):
        ll = DLList(13)
        ll.push(15)

        with pytest.raises(ValueError):
            ll.insert(14)

    def test_dllist_insert_before(self):
        ll = DLList(14)
        ll.push(16)
        ll.push(17)

        ll.insert(15, before_node=ll.head.next)

        assert len(ll) == 4

        _assert_order_and_values(ll, [14, 15, 16, 17])

    def test_dllist_insert_after(self):
        ll = DLList(14)
        ll.push(15)
        ll.push(17)

        ll.insert(16, after_node=ll.tail.prev)

        assert len(ll) == 4

        _assert_order_and_values(ll, [14, 15, 16, 17])


class TestDLListIterator:
    def test_dlliter_init(self):
        ll = DLList(4)
        dlli = DLListIterator(ll)

        assert dlli.dllist is ll
        assert dlli.current is ll.head

    def test_dlliter_iter(self):
        ll = DLList(4)
        dlli = DLListIterator(ll)

        assert dlli.__iter__() is dlli
        assert dlli.__next__() is ll.unshift()

    def test_dlliter_for(self):
        ll = DLList("4")
        ll.push("2")

        ll_iter = iter(ll)

        for i in ll_iter:
            assert i == "4" or i == "2"

        with pytest.raises(StopIteration):
            next(ll_iter)
