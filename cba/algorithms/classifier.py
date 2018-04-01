import pandas as pd

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


    def inspect(self):
        
        dictionary = {
            "lhs": [],
            "rhs": [],
            "confidence": [],
            "support": [],
            "length": []
        }

        for rule in self.rules:
            dictionary["lhs"].append(rule.antecedent.string())
            dictionary["rhs"].append(rule.consequent.string())
            dictionary["confidence"].append(rule.confidence)
            dictionary["support"].append(rule.support)
            dictionary["length"].append(len(rule.antecedent) + 1)

        rules_df = pd.DataFrame(dictionary)
        rules_df = rules_df[["lhs", "rhs", "confidence", "support", "length"]]

        return rules_df

