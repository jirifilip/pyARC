from .comparable_itemset import ComparableItemSet
from .item import Item

class Consequent(Item, ComparableItemSet):
    """
    Represents a right-hand side of the association rule.
    """
    
    def getclass(self):
        return self.value
    
    def __len__(self):
        return 1
    
    def __repr__(self):
        item_tuple = self.attribute, self.value
        return "Consequent{{{}}}".format(item_tuple)