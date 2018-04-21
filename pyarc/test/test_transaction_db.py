import unittest

from pyarc.data_structures import (
    TransactionDB,
    Transaction,
    Item,
    Antecedent
)

class TestTransactionDB(unittest.TestCase):

    def test_init(self):
        rows1 = [
            [1, 1, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 0, 1]
        ]
        header1 = ["A", "B", "C", "Y"]

        transDB1 = TransactionDB(rows1, header1, unique_transactions=False)

        transaction1 = Transaction([1, 1, 0], "ABC", Item("Y", 0))

        class_labels = [
            Item("Y", 0),
            Item("Y", 1),
            Item("Y", 1),
            Item("Y", 1),
        ]

        assert transDB1.class_labels == class_labels
        assert transDB1.classes == ["0", "1", "1", "1"]
        assert transDB1.data[0] == transaction1


    def test_len(self):
        rows1 = [
            [1, 1, 0, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 1],
            [0, 1, 0, 1]
        ]
        header1 = ["A", "B", "C", "Y"]

        transDB1 = TransactionDB(rows1, header1)

        assert len(transDB1) == 4