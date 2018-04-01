class Item():
    """
    represents a (attribute, value) pair
    """
    
    def __init__(self, attribute, value):
        self.attribute = repr(attribute) if type(attribute) != str else attribute
        self.value = repr(value) if type(value) != str else value
        
    def _get_tuple(self):
        return (self.attribute, self.value)
    
    def __getitem__(self, idx):
        item = self._get_tuple()
        return item[idx]
    
    
    def __hash__(self):
        """
        returns: (attribute, value) tuple
        """
        return hash(self._get_tuple())
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __lt__(self, other):
        return self._get_tuple() < other._get_tuple()
    
    def __gt__(self, other):
        return self._get_tuple() > other._get_tuple()
    
    def __repr__(self):
        return "Item{{{}}}".format(self._get_tuple())

    def string(self):
        return "{}={}".format(*self)
    
    