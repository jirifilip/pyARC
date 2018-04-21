import pandas as pd
import sklearn.metrics as skmetrics

class Classifier:

    def test_transactions(self, txns):
        pred = self.predict_all(txns)
        actual = txns.classes

        return accuracy_score(pred, actual)

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
            "length": [],
            "id": []
        }

        for rule in self.rules:
            dictionary["lhs"].append(rule.antecedent.string())
            dictionary["rhs"].append(rule.consequent.string())
            dictionary["confidence"].append(rule.confidence)
            dictionary["support"].append(rule.support)
            dictionary["length"].append(len(rule.antecedent) + 1)
            dictionary["id"].append(rule.rid)

        rules_df = pd.DataFrame(dictionary)
        rules_df = rules_df[["lhs", "rhs", "confidence", "support", "length", "id"]]

        return rules_df




from functools import reduce

def accuracy_score(actual, predicted):

    length = len(actual)

    indices = range(length)

    def reduce_indices(previous, current):
        i = current

        result = 1 if actual[i] == predicted[i] else 0

        return previous + result

    accuracy = reduce(reduce_indices, indices) / length

    return accuracy