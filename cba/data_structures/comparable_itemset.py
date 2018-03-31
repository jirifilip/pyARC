class ComparableItemSet:
    
    def issuperset(self, other):
        return frozenset(self) >= frozenset(other)
        
    def issubset(self, other):
        return frozenset(self) <= frozenset(other) 
        
    def __ge__(self, other):
        return self.issuperset(other)
        
    def __le__(self, other):
        return self.issubset(other)
    
    