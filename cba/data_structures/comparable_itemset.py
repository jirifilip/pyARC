class ComparableItemSet:
    
    def issuperset(self, other):
        return self.frozenset >= other.frozenset
        
    def issubset(self, other):
        return self.frozenset <= other.frozenset 
        
    def __ge__(self, other):
        return self.issuperset(other)
        
    def __le__(self, other):
        return self.issubset(other)
    
    