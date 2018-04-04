from .appearance import Appearance
from .transaction import Transaction
from . import Item

class TransactionDB:
    
    def __init__(self, dataset, header):
        """
        arguments:
        - dataset: [[primitive]]
        - header: [string] - feature labels
        
        assert:
        - len(header) == len(values_list)
        
        """
        
        self.class_labels = []
        
        new_dataset = []

        for row in dataset:
            class_label = Item(header[-1], row[-1])
            new_row = Transaction(row[:-1], header[:-1], class_label)
            
            self.class_labels.append(class_label)
            
            new_dataset.append(new_row)
            
        self.data = new_dataset
        self.classes = list(map(lambda i: i[1], self.class_labels))
        
        
        
        get_string_items = lambda transaction: transaction.string_items
        
        mapped = map(get_string_items, self)
        
        self.string_representation = list(mapped)
        
        

    @property
    def appeardict(self):
        appear = Appearance()
        
        unique_class_items = set(self.class_labels)
        
        for item in unique_class_items:
            appear.add_to_RHS(item)

        return appear.dictionary
        
    
    def __getitem__(self, idx):
        return self.data[idx]
    
    
    @classmethod
    def from_pandasdf(clazz, df):
        """
        convert pandas dataframe to DataSet
        """
        
        rows = df.values
        header = list(df.columns.values)

        return clazz(rows, header)

    
    def __repr__(self):
        return repr(self.string_representation)
        
    def __len__(self):
        return len(self.data)
        
