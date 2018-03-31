import pandas as pd

from cba import CBA
from cba.data_structures import TransactionDB

df = pd.read_csv("c:/code/python/machine_learning/assoc_rules/train/iris0.csv")
transactions = TransactionDB.from_pandasdf(df) 
transactions_test = TransactionDB.from_pandasdf(pd.read_csv("c:/code/python/machine_learning/assoc_rules/test/iris0.csv"))

cba = CBA()

pred = cba.fit(transactions).predict(transactions_test)

print(pred)