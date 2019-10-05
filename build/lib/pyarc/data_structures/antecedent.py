from functools import reduce
from .comparable_itemset import ComparableItemSet

class Antecedent(ComparableItemSet):
    """Antecedent represents a left-hand side of the association rule.
    It is a set of conditions (Items) a Transaction has to satisfy.

    Parameters
    ----------
    items: 1D array of Items


    Attributes
    ----------
    itemset: 1D array of Items
        dictionary of unique attributes, such as: {a: 1, b: 3}

    frozenset: frozenset of Items
        this attribute is vital for determining if antecedent
        is a subset of transaction and, consequently, if transaction
        satisfies antecedent

    """
    
    def __init__(self, items):

        # extract unique attributes and convert them to dict
        # such as: {a: 1, b: 3, c: 4}
        self.itemset = dict(list(set(items)))

        # this part is important for better performance
        # of M1 and M2 algoritms
        self.frozenset = frozenset(self)
        
    
    def __getattr__(self, attr_name):
        """
        Parameters
        ----------
        attribute: str
            name of desired attribute

        Returns
        -------
        Attribute of given name, otherwise an AttributeError
        """
        item = self.itemset.get(attr_name, None)
        
        if (item):
            return item
        else:
            raise AttributeError("No attribute of that name")
            
    
    def __getitem__(self, idx):
        """Method which allows indexing on antecedent's itemset
        """
        items = list(self.itemset.items())
        
        if (idx <= len(items)):
            return items[idx]
        else:
            raise IndexError("No value at the specified index")

    def __len__(self):
        """
        Returns
        -------
        length of the itemset
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