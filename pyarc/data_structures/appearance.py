class Appearance:
    """Appearance represents an easy way to get an appearance 
    dictionary for functions from fim package.


    Attributes
    ----------
    self.lhs: array of (string, string)

    self.rhs: array of (string, string)

    frozenset: frozenset of Items
        this attribute is vital for determining if antecedent
        is a subset of transaction and, consequently, if transaction
        satisfies antecedent

    """
    
    def __init__(self):
        self.lhs = []
        self.rhs = []
        
        
    def add_to_LHS(self, item):
        self.__add(item, "a")
        
    def add_to_RHS(self, item):
        self.__add(item, "c")
        
    def __add(self, item, where):
        """
        Function for adding a condition to either self.rhs
        or self.lhs
        """

        key, value = item.attribute, item.value
        string_repr = "{}:=:{}".format(key, value)
        
        # finding to which side we need to insert
        where_list = self.lhs if where == "a" else self.rhs
        
        # inserting a condition
        where_list.append((string_repr, where))
        
        
    @property
    def dictionary(self):
        """
        Get a final dictionary to be used in functions 
        from fim package.
        """
        if not self.lhs:
            self.lhs.append((None, "a"))
            
        if not self.rhs:
            self.rhs.append((None, "c"))
            
        appear_list = self.lhs + self.rhs
        
        return dict(appear_list)
