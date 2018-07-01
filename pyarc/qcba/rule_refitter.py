class RuleReffiter:
    
    def __init__(self, undiscretized_values_df):
        self.undiscretized_values_df = undiscretized_values_df
        
    def refit(self, quant_rules):
        for quant_rule in quant_rules:
            self.process_rule(quant_rule)
            
        return quant_rules
            
    
    
    def process_rule(self, quant_rule):
        for idx, (attr, interval) in enumerate(quant_rule.new_antecedent):
            
            current_attribute_values = self.undiscretized_values_df[[attr]].values

            refitted_interval = interval.refit(current_attribute_values)

            quant_rule.new_antecedent[idx] = attr, refitted_interval