import pandas as pd
from functools import reduce

from ..data_structures import ClassAssocationRule, Antecedent, Consequent

class Classifier:
    """
    Classifier for CBA that can predict 
    class labels based on a list of rules.
    """

    def __init__(self):
        self.rules = []
        self.default_class = None
        self.default_class_attribute = None
        self.default_class_confidence = None
        self.default_class_support = None

        self.default_rule = None



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

    def predict_matched_rule(self, datacase):
        """returns a rule that matched the instance
        according to the CBA order (rules are sorted
        by confidence, support and length and first matched
        rule is returned)
        """
        for rule in self.rules:
            if rule.antecedent <= datacase:
                return rule

        return self.default_rule

    def predict_matched_rule_all(self, dataset):
        """for each data instance, returns a rule that
        matched it according to the CBA order (sorted by 
        confidence, support and length)
        """
        matched_rules = []
        
        for datacase in dataset:
            matched_rules.append(self.predict_matched_rule(datacase))
            
        return matched_rules



    def predict_probability(self, datacase):
        """predicts target class probablity of one 
        datacase
        """
        for rule in self.rules:
            if rule.antecedent <= datacase:
                return rule.confidence
            
        return self.default_class_confidence

    def predict_probability_all(self, dataset):
        """predicts target class probablity
        of an array of datacases
        """
        predicted = []
        
        for datacase in dataset:
            predicted.append(self.predict_probability(datacase))
            
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

        # default rule
        dictionary["lhs"].append("{}")
        dictionary["rhs"].append(self.default_class)
        dictionary["confidence"].append(self.default_class_confidence)
        dictionary["support"].append(self.default_class_support)
        dictionary["length"].append(1)
        dictionary["id"].append(None)


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