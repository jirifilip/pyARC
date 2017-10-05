class CBAClassifier:
    
    def __init__(self):
        self.rules = []
        self.default_class = 0
        self.error_number = 0
        
    def add_rule(self, rule):
        self.rules.append(rule)
        
    def add_default_class(self, default_class):
        self.default_class = default_class
        
    def test_dataset(self, dataset, y):
        for idx, datacase in enumerate(dataset):
            current_y = y[idx]
            classified_y, rule = self.classify_datacase(datacase)
            if not (current_y == classified_y):
                if rule is not None:
                    rule.error_number += 1
                self.error_number += 1
            
            
    def classify_datacase(self, datacase):
        for rule in self.rules:
            if rule.condset <= datacase:
                return rule.y, rule
        return self.default_class, None
    
    
    def predict(self, datacase):
        prediction, _ = self.classify_datacase(datacase)
        return prediction
    
    