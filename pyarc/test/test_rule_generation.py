import unittest
from pyarc.data_structures import (
    Item,
    Antecedent,
    Consequent,
    ClassAssocationRule,
    Transaction,
    TransactionDB
)
from pyarc.algorithms import (
    createCARs,
    generateCARs,
    top_rules,
    
)
from utils import HiddenPrints



class TestRuleGeneration(unittest.TestCase):


    def test_generateCARs(self):
        header1 = ["A", "B", "Y"]
        rows1 = [
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 1]
        ]

        transactionDB1 = TransactionDB(rows1, header1)

        rules = generateCARs(transactionDB1, support=50)

        car1 = ClassAssocationRule([], Consequent("Y", 1), support=0.5, confidence=0.5)
        car1.id = rules[0].id

        car2 = ClassAssocationRule([], Consequent("Y", 0), support=0.5, confidence=0.5)
        car1.id = rules[1].id

        car1 == rules[0]
        car2 == rules[1]



    def test_createCARs(self):
        
        generated_rules = [
            ('Y:=:1', (), 0.5, 0.5),
            ('Y:=:0', (), 0.5, 0.5),
            ('Y:=:1', ('A:=:1',), 0.5, 1 / 3)
        ]

        cars = createCARs(generated_rules)

        assert cars[0].consequent == Consequent("Y", 1)
        assert cars[0].confidence == 0.5
        assert cars[0].support == 0.5

        assert cars[1].consequent == Consequent("Y", 0)
        assert cars[1].confidence == 0.5
        assert cars[1].support == 0.5


        assert cars[2].consequent == Consequent("Y", 1)
        assert cars[2].antecedent == Antecedent([Item("A", 1)])
        assert cars[2].confidence == 1 / 3
        assert cars[2].support == 0.5


    def test_top_rules(self):
        header1 = ["A", "B", "Y"]
        rows1 = [
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 1]
        ]

        transactionDB1 = TransactionDB(rows1, header1)

        rules = None
        with HiddenPrints():
            rules = top_rules(transactionDB1.string_representation, appearance=transactionDB1.appeardict)

        expected_rules = [
            ('Y:=:1', ('A:=:1',), 1/6, 1/3),
            ('Y:=:0', ('A:=:1',), 1/3, 2/3),
            ('Y:=:1', ('B:=:1',), 1/6, 1/3),
            ('Y:=:0', ('B:=:1',), 1/3, 2/3),
            ('Y:=:1', ('B:=:1', 'A:=:1'), 1/6, 1/3),
            ('Y:=:0', ('B:=:1', 'A:=:1'), 1/3, 2/3),
            ('Y:=:1', ('A:=:0',), 1/3, 2/3),
            ('Y:=:0', ('A:=:0',), 1/6, 1/3),
            ('Y:=:1', ('B:=:0',), 1/3, 2/3),
            ('Y:=:0', ('B:=:0',), 1/6, 1/3),
            ('Y:=:1', ('B:=:0', 'A:=:0'), 1/3, 2/3),
            ('Y:=:0', ('B:=:0', 'A:=:0'), 1/6, 1/3)
        ]

        for r in rules:
            assert r in expected_rules



