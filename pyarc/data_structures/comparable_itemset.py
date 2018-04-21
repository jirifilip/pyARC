class ComparableItemSet:
    """ ComparableItemSet is a common ancestor
    for Antecedent and Transaction class so that
    they both can be compared using <= and >= 
    operators.

    Any class that inherits from ComparableItemSet
    needs to have a "frozenset" attribute. "frozenset"
    attribute is a frozenset of Items and allows easy 
    comparing and determining if one ComparableItemSet
    is a subset or superset of another ComparableItemSet.

    """

    def issuperset(self, other):
        return self.frozenset >= other.frozenset
        
    def issubset(self, other):
        return self.frozenset <= other.frozenset 
        
    def __ge__(self, other):
        return self.issuperset(other)
        
    def __le__(self, other):
        return self.issubset(other)
    
    