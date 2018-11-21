from .data_structures import QuantitativeDataFrame
from sklearn.metrics import accuracy_score

class QuantitativeClassifier:
    
    def __init__(self, rules, default_class):
        self.rules = rules
        self.default_class = default_class
        
        
    def rule_model_accuracy(self, quantitative_dataframe, ground_truth):
        predicted = self.predict(quantitative_dataframe)

        return accuracy_score(predicted, ground_truth)

    def predict(self, quantitative_dataframe):
        predicted_classes = []
    
        for _, row in quantitative_dataframe.dataframe.iterrows():
            appended = False
            for rule in self.rules:
                antecedent_dict = dict(rule.antecedent)  
                counter = True

                for name, value in row.iteritems():
                    if name in antecedent_dict:
                        interval = antecedent_dict[name]

                        if type(interval) == str:
                            counter &= interval == value
                        else:
                            result = interval.isin(value)
                            counter &= result

                if counter:
                    _, predicted_class = rule.consequent
                    predicted_classes.append(predicted_class)
                    appended = True
                    break
                    
            if not appended:
                predicted_classes.append(self.default_class)

                    
        return predicted_classes            



