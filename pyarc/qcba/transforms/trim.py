class RuleTrimmer:
    """Trims the rule
    """
    
    
    def __init__(self, quantitative_dataframe):
        self.__dataframe = quantitative_dataframe
        
        
    def transform(self, rules):
        copied_rules = [ rule.copy() for rule in rules  ]
        trimmed = [ self.__trim(rule) for rule in copied_rules ]
        
        return trimmed
    
    
    def __trim(self, rule):
        if type(rule) != QuantitativeCAR:
            raise Exception("type of rule must be QuantClassAssociationRule")

            
        covered_by_antecedent_mask, covered_by_consequent_mask = self.__dataframe.find_covered_by_rule_mask(rule)
        
        covered_by_rule_mask = covered_by_antecedent_mask & covered_by_consequent_mask
        
        # instances covered by rule
        correctly_covered_by_r = self.__dataframe.mask(covered_by_rule_mask)
        
        antecedent = rule.antecedent

        for idx, literal in enumerate(antecedent):

            attribute, interval = literal
            
            current_column = correctly_covered_by_r[[attribute]].values
            current_column_unique = np.unique(current_column)

            if not current_column.any():
                continue

            minv = np.asscalar(min(current_column))
            maxv = np.asscalar(max(current_column))

            new_interval = Interval(minv, maxv, True, True)

            antecedent[idx] = attribute, new_interval

        return rule
    
    