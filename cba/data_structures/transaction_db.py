from .appearance import Appearance
from .transaction import Transaction, UniqueTransaction
from . import Item

class TransactionDB:
    
    def __init__(self, dataset, header, unique_transactions=False):
        """
        arguments:
        - dataset: [[primitive]]
        - header: [string] - feature labels
        
        assert:
        - len(header) == len(values_list)
        
        """
        
        TransactionClass = UniqueTransaction if unique_transactions else Transaction
        
        self.header = header
        self.class_labels = []
        
        new_dataset = []

        for row in dataset:
            class_label = Item(header[-1], row[-1])
            new_row = TransactionClass(row[:-1], header[:-1], class_label)
            
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
    def from_DataFrame(clazz, df, unique_transactions=False):
        """
        convert pandas dataframe to DataSet
        """
        
        rows = df.values
        header = list(df.columns.values)

        return clazz(rows, header, unique_transactions=unique_transactions)

    
    def __repr__(self):
        return repr(self.string_representation)
        
    def __len__(self):
        return len(self.data)
        
