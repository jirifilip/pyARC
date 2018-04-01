import unittest
from cba.data_structures import (
    Item,
    Antecedent,
    Consequent,
    ClassAssocationRule,
    Appearance
)

class TestAppearance(unittest.TestCase):

    def test_adding(self):

        item1 = Item("A", 1)
        item2 = Item("B", 1)
        item3 = Item("C", 0)
        item4 = Item("B", 5)

        appear1 = Appearance()
        appear1.add_to_LHS(item1)
        appear1.add_to_LHS(item2)

        assert appear1.lhs == [("A=1", "a"), ("B=1", "a")]
        
        appear1.add_to_RHS(item3)

        assert appear1.rhs == [("C=0", "c")]

        appear1.rhs = [("B=5", "c")]

        assert appear1.rhs == [("B=5", "c")]

        dictionary = appear1.dictionary

        assert dictionary == dict([("A=1", "a"), ("B=1", "a"), ("B=5", "c")])

        appear1.lhs = []
        dictionary2 = appear1.dictionary


        assert dictionary2 == dict([(None, "a"), ("B=5", "c")])
