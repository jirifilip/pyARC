class Classifier:
    
    def init(self):
        self.rules = []
        self.default_class = None
        
    def predict(self, datacase):
        for rule in self.rules:
            if rule.antecedent <= datacase:
                return rule.consequent.value
            
        return self.default_class    
        
    def predict_all(self, dataset):
        predicted = []
        
        for datacase in dataset:
            predicted.append(self.predict(datacase))
            
        return predicted