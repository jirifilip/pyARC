import pandas
import numpy as np

from ..data_structures import QuantitativeDataFrame, Interval


class RuleOverlapPruner:
    
    def __init__(self, quantitative_dataset):
        self.__dataframe = quantitative_dataset
        
        
    def transform(self, rules, default_class, transaction_based=True):
        copied_rules = [ rule.copy() for rule in rules ]

        pruned_rules = copied_rules

        if transaction_based:
            pruned_rules = self.prune_transaction_based(copied_rules, default_class)        
        else:
            pruned_rules = self.prune_range_based(copied_rules, default_class)

        return pruned_rules
    
    def prune_transaction_based(self, rules, default_class):
        """Transaction based
        """
        
        new_rules = [ rule for rule in rules ]
        
        for idx, rule in enumerate(rules):
            
            rule_classname, rule_classval = rule.consequent
            
            if rule_classval != default_class:
                print("not including", rule)
                continue

            print(rule)            

            correctly_covered_antecedent, correctly_covered_consequent = self.__dataframe.find_covered_by_rule_mask(rule)
            correctly_covered = correctly_covered_antecedent & correctly_covered_consequent

            print(correctly_covered)
            
            non_empty_intersection = False
            
            for candidate_clash in rules[idx:]:
                
                cand_classname, cand_classval = candidate_clash.consequent
                
                if cand_classval == default_class:
                    continue
                    
                print(candidate_clash)    
                cand_clash_covered_antecedent, cand_clash_covered_consequent = self.__dataframe.find_covered_by_rule_mask(candidate_clash)
                
                print("any", any(cand_clash_covered_antecedent & correctly_covered))
                
                if any(cand_clash_covered_antecedent & correctly_covered):
                    non_empty_intersection = True
                    break
                    
            if non_empty_intersection == False:
                new_rules.remove(rule)
                
            
        return new_rules
        
    
    
    

    
    def prune_range_based(self, rules, default_class):
        
        """Transaction based
        """
        
        new_rules = []
        
        for idx, rule in enumerate(rules):
            
            rule_classname, rule_classval = rule.consequent
            
            if rule_classval != default_class:
                continue
                            
            literals = dict(rule.antecedent)
            attributes = literals.keys()

            clashing_rule_found = False
            
            """
            correctly_covered_antecedent, correctly_covered_consequent = self.__dataframe.find_covered_by_rule_mask(rule)
            correctly_covered = correctly_covered_antecedent & correctly_covered_consequent
            """
            non_empty_intersection = False
            
            
            for candidate_clash in rules[idx:]:
                
                cand_classname, cand_classval = candidate_clash.consequent
                
                if cand_classval == default_class:
                    continue
                    
                attributes_candclash = dict(candidate_clash.antecedent).keys()
                shared_attributes = set(attributes) & set(attributes_candclash)
                
                if not shared_attributes:
                    clashing_rule_found = True
                    break
                    
                clash_cand_antecedent_dict = dict(candidate_clash.antecedent)
                literals_in_clash_shared_att = [ (key, clash_cand_antecedent_dict[key]) for key in shared_attributes  ]
                
                at_least_one_attribute_disjunct = False
                
                for literal in literals_in_clash_shared_att:
                    attribute, value = literal
                    
                    temp_literal = attribute, literals[attribute]
                    
                    
                    
            if non_empty_intersection == False:
                new_rules.remove(rule)
                
            
        return new_rules