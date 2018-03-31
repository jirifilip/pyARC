from .comparable_itemset import ComparableItemSet
from . import Item

class Transaction(ComparableItemSet):
    
    def __init__(self, row, header, class_item):
        self.class_val = class_item
        self.items = []
        
        self.alreadycovered = False
        self.hidden = False
        
        # eg. [pay=high, eyes=green]
        self.string_items = []
        
        
        for idx, val in enumerate(row):
            header_label = header[idx]
            
            item = Item(header_label, val)
            
            self.string_items.append("{}={}".format(header_label, val)) 
            
            self.items.append(item)
            
        key, val = self.class_val
        self.string_items.append("{}={}".format(key, val))
            
            
    
    def __repr__(self):
        string = ", ".join(self.string_items) 
        return "{" + string + "}"
    
    def __hash__(self):
        return hash(tuple(self.items))
    
    def __getitem__(self, idx):
        return self.items[idx]
    
    def getclass(self):
        return self.class_val