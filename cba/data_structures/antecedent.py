from functools import reduce
from .comparable_itemset import ComparableItemSet

class Antecedent(ComparableItemSet):
    """Antecedent represents a left-hand side of the association rule.
    It is a set of conditions (Items) a Transaction has to satisfy.
    """
    
    def __init__(self, items):
        """
        items: list of conditions
        """
        self.itemset = dict(list(set(items)))

        self.frozenset = frozenset(self)
        
    
    def __getattr__(self, attr_name):
        item = self.itemset.get(attr_name, None)
        
        if (item):
            return item
        else:
            raise AttributeError("No attribute of that name")
            
    
    def __getitem__(self, idx):
        """
        method that supports indexing
        """
        items = list(self.itemset.items())
        
        if (idx <= len(items)):
            return items[idx]
        else:
            raise IndexError("No value at the specified index")
            
    def __len__(self):
        """
        returns: length of itemset
        """
        return len(self.itemset)
            
    def __repr__(self):
        str_array = [repr((attr, val)) for attr, val in self.itemset.items()]
        text = ", ".join(str_array)
        return "Antecedent({})".format(text)
    
    def __hash__(self):
        return hash(tuple(self.itemset.items()))
    
    def __eq__(self, other):
        return hash(self) == hash(other)

    def string(self):
        items = list(self.itemset.items())
        string_items = [ "{}={}".format(key, val) for key, val in items ]

        string_ant = ",".join(string_items)

        return "{" + string_ant + "}"