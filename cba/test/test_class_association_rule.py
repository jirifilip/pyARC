import unittest
from cba.data_structures import (
    Item,
    Antecedent,
    Consequent,
    ComparableItemSet,
    ClassAssocationRule,
    Transaction
)

class TestClassAssociationRule(unittest.TestCase):

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

        cons1 = Consequent("Y", 1)
        cons2 = Consequent("Y", 2)
        cons3 = Consequent("Y", 3)

        # len: 2
        car1 = ClassAssocationRule(ant1, cons1, 0.5, 0.9)
        # len: 1
        car2 = ClassAssocationRule(ant2, cons2, 0.5, 0.9)

        car3 = ClassAssocationRule(ant3, cons3, 0.5, 0.9)
        car4 = ClassAssocationRule(ant4, cons3, 0.5, 1)

        sorted_cars = sorted([car1, car2, car3, car4], reverse=True)
        
        assert car1 < car2
        assert car2 > car3
        assert car3 < car2
        assert car4 > car3
        assert car1.antecedent <= transaction1
        assert car2.antecedent <= transaction1
        assert car3.antecedent <= transaction1
        assert not car4.antecedent <= transaction1
        assert sorted_cars[0] == car4

    def test_len(self):
        
        item1 = Item("A", 1)
        item2 = Item("B", 1)

        ant1 = Antecedent([item1, item2])

        cons1 = Consequent("Y", 1)

        car1 = ClassAssocationRule(ant1, cons1, 0.5, 0.9)

        assert len(car1) == 3
