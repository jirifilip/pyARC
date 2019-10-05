from .comparable_itemset import ComparableItemSet
from .item import Item
import pandas as pd
import numpy as np


class Transaction(ComparableItemSet):
    """Transaction represents one instance in a dataset.
    Transaction is hashed based on its items and class 
    value. 

    Parameters
    ----------
    
    row: array of ints or strings

    header: array of strings
        Represents column labels.
    
    class_item: Item
        Item with class attribute.

    drop_NaN: bool
        Used for determining whether a an Item
        with NULL value should be dropped from Transaction


    Attributes
    ----------
    items: array of Items

    tid: int
        Transaction ID.

    alreadycovered: bool
        Used in M2Algorithm for determining if the transaction
        was already covered by some other rule.

    string_items: two dimensional array of strings
        e.g. [["a:=:1", "b:=:2"]]




    """


    id_ = 0
    
    def __init__(self, row, header, class_item, drop_NaN=True):
        self.class_val = class_item
        self.items = []
        self.tid = Transaction.id_
        Transaction.id_ += 1
        
        self.alreadycovered = False
        
        # eg. [pay=high, eyes=green]
        self.string_items = []
        
        
        for idx, val in enumerate(row):
            # Drop items with NULL value
            if drop_NaN and pd.isnull(val):
                continue

            header_label = header[idx]
            
            item = Item(header_label, val)
            
            self.string_items.append("{}:=:{}".format(header_label, val)) 
            
            self.items.append(item)
            
        key, val = self.class_val
        self.string_items.append("{}:=:{}".format(key, val))

        self.frozenset = frozenset(self)
            
            
    
    def __repr__(self):
        string = ", ".join(self.string_items) 
        return "{" + string + "}"
    
    def __hash__(self):
        return hash(tuple(self.items))
        #return hash((self.tid, tuple(self.items)))

    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __getitem__(self, idx):
        return self.items[idx]
    
    def getclass(self):
        return self.class_val



class UniqueTransaction(Transaction):
    """Same as Transaction class except for
    hashing by Transaction id. 

    """
    def __hash__(self):
        return hash(self.tid)