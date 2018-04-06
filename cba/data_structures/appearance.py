class Appearance:
    
    def __init__(self):
        self.lhs = []
        self.rhs = []
        
        
    def add_to_LHS(self, item):
        self.__add(item, "a")
        
    def add_to_RHS(self, item):
        self.__add(item, "c")
        
    def __add(self, item, where):
        key, value = item.attribute, item.value
        string_repr = "{}:=:{}".format(key, value)
        
        where_list = self.lhs if where == "a" else self.rhs
        
        where_list.append((string_repr, where))
        
        
    @property
    def dictionary(self):
        if not self.lhs:
            self.lhs.append((None, "a"))
            
        if not self.rhs:
            self.rhs.append((None, "c"))
            
        appear_list = self.lhs + self.rhs
        
        return dict(appear_list)
