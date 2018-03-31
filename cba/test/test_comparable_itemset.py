import unittest
from cba.data_structures import (
    Item,
    Antecedent,
    ComparableItemSet,
    Transaction
)

class TestComparableItemSet(unittest.TestCase):

    def test_compare(self):

        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction1 = Transaction(row1, header1, ("Class", 0))

        item1 = Item("A", 1)
        item2 = Item("B", 1)
        item3 = Item("C", 0)
        item4 = Item("B", 5)

        ant1 = Antecedent([item1, item2])
        ant2 = Antecedent([item2])
        ant3 = Antecedent([item3])
        ant4 = Antecedent([item4])

        assert ant1 <= transaction1
        assert ant2 <= transaction1
        assert ant3 <= transaction1
        self.assertFalse(ant4 <= transaction1)

        assert transaction1 >= ant1
        assert transaction1 >= ant2
        assert transaction1 >= ant3

