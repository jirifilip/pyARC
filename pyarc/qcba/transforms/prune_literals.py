class RuleLiteralPruner:
    
    def __init__(self, quantitative_dataframe):
        self.__dataframe = quantitative_dataframe
        
        
    def transform(self, rules):
        copied_rules = [ rule.copy() for rule in rules  ]
        trimmed = [ self.__trim(rule) for rule in copied_rules ]
        
        return trimmed
    
    
    def produce_combinations(self, array):
        arr_len = len(array)
    
        for i in range(arr_len):
            combination = array[0:i] + array[i+1:arr_len]
        
            yield combination
    
    
    def __trim(self, rule):
        if type(rule) != QuantitativeCAR:
            raise Exception("type of rule must be QuantClassAssociationRule")

            
        attr_removed = False
    
        literals = rule.antecedent
        consequent = rule.consequent
        
        rule.update_properties(self.__dataframe)
        
        dataset_len = self.__dataframe.size

        if len(literals) < 1:
            return rule

        while True:
            for literals_combination in self.produce_combinations(literals):
                if not literals_combination:
                    continue
                    
                copied_rule = rule.copy()
                
                copied_rule.antecedent = literals_combination
                copied_rule.update_properties(self.__dataframe)

                if copied_rule.confidence > rule.confidence:
                    rule.support = copied_rule.support
                    rule.confidence = copied_rule.confidence
                    rule.rulelen = copied_rule.rulelen
                    
                    rule.antecedent = copied_rule.antecedent

                    attr_removed = True
                    
                    break
                    
                else:
                    attr_removed = False

            if attr_removed == False:
                break
                
                
        return rule