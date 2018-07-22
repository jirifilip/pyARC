import pandas
import numpy as np

from ..data_structures import QuantitativeDataFrame, Interval


class RuleRefitter:
    """Refits the rule to a finer grid
    """
    
    
    def __init__(self, quantitative_dataframe):
        self.__dataframe = quantitative_dataframe
        
        
    def transform(self, rules):
        copied_rules = [ rule.copy() for rule in rules  ]
        refitted = [ self.__refit(rule) for rule in copied_rules ]
        
        return refitted
        
    def __refit(self, rule):
        """refits a single rule
        """

        for idx, literal in enumerate(rule.antecedent):
            attribute, interval = literal
        
            current_attribute_values = self.__dataframe.column(attribute)

            refitted_interval = interval.refit(current_attribute_values)

            rule.antecedent[idx] = attribute, refitted_interval
            
            
        return rule
            