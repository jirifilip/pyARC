import unittest
import pandas as pd
from pyarc import CBA
from pyarc.data_structures import (
    TransactionDB
)
import os

dataset_file = os.path.dirname(os.path.realpath(__file__)) + "/data/movies_discr.csv"

class TestClassifier(unittest.TestCase):

    def test_inspect(self):
        cba = CBA()

        test_dataframe = pd.read_csv(dataset_file, sep=";")
        
        transactions = TransactionDB.from_DataFrame(test_dataframe)

        cba.fit(transactions)

        clf = cba.clf

        inspect_df = clf.inspect()

        self.assertEqual(type(inspect_df), pd.DataFrame)
        self.assertEqual(len(inspect_df), len(clf.rules) + 1)

        self.assertEqual(inspect_df["lhs"].iloc[-1], "{}")


    def test_default_rule_correct(self):
        cba = CBA(support=0.9)
        cba_m2 = CBA(support=0.9)

        header1 = ["A", "B", "Y"]
        rows1 = [
            [1, 1, 0],
            [0, 0, 1],
        ]

        transactions = TransactionDB(rows1, header1)

        cba.fit(transactions)
        cba_m2.fit(transactions)

        default_class = cba.clf.default_class
        default_class_m2 = cba_m2.clf.default_class

        self.assertTrue(default_class in ["0", "1"])
        self.assertTrue(default_class_m2 in ["0", "1"])

        default_class_support = cba.clf.default_class_support
        default_class_confidence = cba.clf.default_class_confidence
        
        default_class_support_m2 = cba_m2.clf.default_class_support
        default_class_confidence_m2 = cba_m2.clf.default_class_confidence

        self.assertTrue(0 <= default_class_support <= 1)
        self.assertTrue(0 <= default_class_support_m2 <= 1)
        self.assertTrue(0 <= default_class_confidence <= 1)
        self.assertTrue(0 <= default_class_confidence_m2 <= 1)


    def test_predict_probablity(self):
        header1 = ["A", "B", "Y"]
        rows1 = [
            [1, 1, 0],
            [1, 1, 0],
            [1, 1, 1],
            [0, 0, 0],
            [0, 0, 1],
            [0, 0, 1]
        ]

        transactions = TransactionDB(rows1, header1)

        cba = CBA()

        cba.fit(transactions)
        
        probs = cba.clf.predict_probability_all(transactions)