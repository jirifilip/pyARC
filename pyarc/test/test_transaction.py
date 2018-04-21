import unittest

from pyarc.data_structures import (
    Transaction,
    UniqueTransaction,
    Item,
    Antecedent
)

class TestTransaction(unittest.TestCase):

    def test_init(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction1 = Transaction(row1, header1, ("Class", 0))
        transaction2 = UniqueTransaction(row1, header1, ("Class", 0))


    def test_getclass(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction1 = Transaction(row1, header1, ("Class", 0))

        assert transaction1.getclass() == ("Class", 0)


    def test_unique_hash(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction2 = UniqueTransaction(row1, header1, ("Class", 0))
    
        hash(transaction2) == hash(transaction2.tid)

    def test_getitem(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction1 = Transaction(row1, header1, ("Class", 0))

        assert transaction1[0] == Item("A", 1)
        assert transaction1[1] == Item("B", 1)
        assert transaction1[2] == Item("C", 0)

    def test_hash(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        row2 = [1, 1, 0]
        header2 = ["A", "B", "C"]

        row3 = [1, 1, 1]
        header3 = "cde"

        transaction1 = Transaction(row1, header1, ("Class", 0))
        transaction2 = Transaction(row2, header2, ("Class", 0))
        transaction3 = Transaction(row3, header3, ("Class", 2))

        assert transaction1 == transaction2
        assert transaction1 != transaction3
        assert transaction2 != transaction3


    def test_string_items(self):
        row1 = [1, 1, 0]
        header1 = ["A", "B", "C"]

        transaction1 = Transaction(row1, header1, ("Y", 0))

        assert transaction1.string_items == ["A:=:1", "B:=:1", "C:=:0", "Y:=:0"]