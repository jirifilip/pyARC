import pandas as pd
from functools import reduce

class Classifier:
    """
    Classifier for CBA that can predict 
    class labels based on a list of rules.
    """

    def __init__(self):
        self.rules = []
        self.default_class = None


    def test_transactions(self, txns):
        """Takes a TransactionDB and outputs
        accuracy of the classifier
        """
        pred = self.predict_all(txns)
        actual = txns.classes

        return accuracy_score(pred, actual)
    
        
    def predict(self, datacase):
        """predicts target class of one 
        datacase
        """
        for rule in self.rules:
            if rule.antecedent <= datacase:
                return rule.consequent.value
            
        return self.default_class    
        
    def predict_all(self, dataset):
        """predicts target class of an array
        of datacases
        """
        predicted = []
        
        for datacase in dataset:
            predicted.append(self.predict(datacase))
            
        return predicted


    def inspect(self):
        """inspect uses pandas DataFrame to
        display information about the classifier
        """
        
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



def accuracy_score(actual, predicted):
    """Function for determining accuracy given
    list of predicted classes and actual classes
    """

    length = len(actual)

    indices = range(length)

    def reduce_indices(previous, current):
        i = current

        result = 1 if actual[i] == predicted[i] else 0

        return previous + result

    accuracy = reduce(reduce_indices, indices) / length

    return accuracy