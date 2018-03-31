import unittest
from cba.data_structures import Item, Antecedent

class TestAntecedentClass(unittest.TestCase):

    def test_getattr(self):
        item1 = Item("a", 3)
        item2 = Item("b", 3)
        item3 = Item("c", 2)

        ant1 = Antecedent([item1, item2, item3])

        assert ant1.a == "3"
        assert ant1.b == "3"
        assert ant1.c == "2"


    def test_getitem(self):
        item1 = Item("a", 3)
        item2 = Item("b", 3)
        item3 = Item("c", 2)

        ant1 = Antecedent([item1, item2, item3])

        assert ant1[0] in [item1, item2, item3]
        assert ant1[1] in [item1, item2, item3]
        assert ant1[2] in [item1, item2, item3]

    def test_init(self):
        item1 = Item("a", 3)
        item2 = Item("a", 3)
        item3 = Item("c", 2)

        ant1 = Antecedent([item1, item2, item3])

        assert len(ant1.itemset) == 2

    def test_len(self):
        item1 = Item("a", 3)
        item2 = Item("b", 3)
        item3 = Item("c", 2)
        item4 = Item("c", 4)

        ant1 = Antecedent([item1, item2, item3])
        ant2 = Antecedent([item1, item2, item3, item4])

        assert len(ant1) == 3
        assert len(ant2) == 3

    def test_hash(self):
        item1 = Item("a", 3)
        item2 = Item("b", 3)
        item3 = Item("c", 2)

        ant1 = Antecedent([item1, item2, item3])
        ant2 = Antecedent([item1, item2, item3])

        assert hash(ant1) == hash(ant2)
        assert ant1 == ant2