import unittest
from cba.data_structures import Item

class TestItemClass(unittest.TestCase):

    def test_getitem(self):
        item = Item("a", "1")
        assert item[0] == "a"
        assert item[1] == "1" 

    def test_attributes(self):
        item = Item("a", "1")
        assert item.attribute == "a"
        assert item.value == "1" 

    def test_inttostring(self):
        item = Item("a", 1)
        assert item[1] == "1"

    def test_hash(self):
        item1 = Item("a", 1)
        item2 = Item("a", 1)

        assert hash(item1) == hash(item2)

    def test_equals(self):
        item1 = Item("a", 1)
        item2 = Item("a", 1)

        assert item1 == item2

    def test_repr(self):
        item = Item("a", 1)

        string = "Item{('a', '1')}"

        assert repr(item) == string
