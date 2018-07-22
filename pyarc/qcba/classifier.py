from .data_structures import QuantitativeDataFrame


class QuantitativeClassifier:
    
    def __init__(self, rules, default_class):
        self.rules = rules
        self.default_class = default_class
        
        
    def test(self, quantitative_dataframe):
        predicted_classes = []
    
        for _, row in quantitative_dataframe.dataframe.iterrows():
            appended = False
            for rule in self.rules:
                antecedent_dict = dict(rule.antecedent)  
                counter = True

                for name, value in row.iteritems():
                    if name in antecedent_dict:
                        result = antecedent_dict[name].isin(value)
                        counter &= result

                if counter:
                    _, predicted_class = rule.consequent
                    predicted_classes.append(predicted_class)
                    appended = True
                    break
                    
            if not appended:
                predicted_classes.append(self.default_class)

                    
        return predicted_classes            



