class Item():
    """ Item class for representing attribute-value pair
    and one item in transaction or antecedent.


    Parameters
    ----------
    attribute : str
        name of the item

    value: str
        value of the item


    Attributes
    ----------
    attribute : str
        name of the item

    value: str
        value of the item


    """
    def __init__(self, attribute, value):
        # convert attribute and value so that 
        # Item("a", 1) == Item("a", "1")
        self.attribute = repr(attribute) if type(attribute) != str else attribute
        self.value = repr(value) if type(value) != str else value
        
    def __get_tuple(self):
        """Private method for getting an (attribute, value) pair"""
        return (self.attribute, self.value)
    
    def __getitem__(self, idx):
        """Method for accessing Item as a tuple"""
        item = self.__get_tuple()
        return item[idx]
    
    
    def __hash__(self):
        """Two Items with the same attribute and value
        have identical hash value.
        """
        return hash(self.__get_tuple())
    
    def __eq__(self, other):
        """Overriden method in order to compare based on
        value and not reference.
        """
        return hash(self) == hash(other)
    
    def __repr__(self):
        """Method for representing Item as a string.

        >>> item1 = Item("a", 1)
        >>> repr(item1)
        >>> Item{(a, 1)}
        """

        return "Item{{{}}}".format(self.__get_tuple())

    def string(self):
        """Method for getting simpler representation.
        
        
        >>> item1 = Item("a", 1)
        >>> item1.string()
        >>> a=1
        """
        return "{}={}".format(*self)
    
    