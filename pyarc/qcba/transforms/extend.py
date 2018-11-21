import pandas
import numpy as np
import math

from ..data_structures import QuantitativeDataFrame, Interval

class RuleExtender:
    
    def __init__(self, dataframe):
    
        if type(dataframe) != QuantitativeDataFrame:
            raise Exception(
                "type of dataset must be pandas.DataFrame"
            )
            
        self.__dataframe = dataframe
        
        
        
    def transform(self, rules):
        
        copied_rules = [ rule.copy() for rule in rules ]

        progress_bar_len = 50
        copied_rules_len = len(copied_rules)
        progress_bar = "#" * progress_bar_len
        progress_bar_empty = " " * progress_bar_len
        last_progress_bar_idx = -1

        extended_rules = []

        #print("len: ", copied_rules_len)

        for i, rule in enumerate(copied_rules):
            current_progress_bar_idx = math.floor(i / copied_rules_len * progress_bar_len)
            
            if last_progress_bar_idx != current_progress_bar_idx:
                last_progress_bar_idx = current_progress_bar_idx
                
                progress_string = "[" + progress_bar[:last_progress_bar_idx] + progress_bar_empty[last_progress_bar_idx:] + "]"
                
                print(*progress_string, sep="")

            extended_rules.append(self.__extend(rule))
        
        return extended_rules
    
    
    
    def __extend(self, rule):
        ext = self.__extend_rule(rule)
        
        return ext
        
    def __extend_rule(self, rule, min_improvement=0, min_conditional_improvement=-0.01):
        
        # check improvemnt argument ranges
        
        current_best = rule
        direct_extensions = self.__get_extensions(rule)
        
        current_best.update_properties(self.__dataframe)
        
        while True:
            extension_succesful = False

            direct_extensions = self.__get_extensions(current_best)

            #print("extending - new cycle")
            
            for candidate in direct_extensions:
                #print("\tcandidate - direct extensions")
                candidate.update_properties(self.__dataframe)
                
                delta_confidence = candidate.confidence - current_best.confidence
                delta_support = candidate.support - current_best.support
                
                
                if self.__crisp_accept(delta_confidence, delta_support, min_improvement):
                    current_best = candidate
                    extension_succesful = True
                    break
                    
                
                if self.__conditional_accept(delta_confidence, min_conditional_improvement):
                    enlargement = candidate
                    
                    while True:
                        enlargement = self.get_beam_extensions(enlargement)
                        
                        if not enlargement:
                            break
                            
                        candidate.update_properties(self.__dataframe)
                        enlargement.update_properties(self.__dataframe)

                        delta_confidence = enlargement.confidence - current_best.confidence
                        delta_support = enlargement.support - current_best.support

                        if self.__crisp_accept(delta_confidence, delta_support, min_improvement):
                            current_best = enlargement
                            extension_succesful = True
                            
                        elif self.__conditional_accept(delta_confidence, min_conditional_improvement):
                            continue
                        
                        else:
                            break
            
            
                    if extension_succesful == True:
                        break
                        

                else:
                    # continue to next candidate
                    continue
           
        
            if extension_succesful == False:
                break
                    
        return current_best
        
        
    def __get_extensions(self, rule):
        extended_rules = []
        
        for literal in rule.antecedent:
            attribute, interval = literal
            
            neighborhood = self.__get_direct_extensions(literal)
            
            for extended_literal in neighborhood:
                # copy the rule so the extended literal
                # can replace the default literal
                copied_rule = rule.copy()
                
                # find the index of the literal
                # so that it can be replaced
                current_literal_index = copied_rule.antecedent.index(literal)
                
                copied_rule.antecedent[current_literal_index] = extended_literal
                copied_rule.was_extended = True
                copied_rule.extended_literal = extended_literal
                
                extended_rules.append(copied_rule)

        extended_rules.sort(reverse=True)
             
        return extended_rules
            
    
    def __get_direct_extensions(self, literal):
        """
        ensure sort and unique
        before calling functions
        """
        
        attribute, interval = literal

        # if nominal
        # needs correction to return null and skip when extending
        if type(interval) == str:
            return [literal]
        
        vals = self.__dataframe.column(attribute)
        vals_len = vals.size

        mask = interval.test_membership(vals)

        # indices of interval members
        # we want to extend them 
        # once to the left
        # and once to the right
        # bu we have to check if resulting
        # indices are not larger than value size
        member_indexes = np.where(mask)[0]

        first_index = member_indexes[0]
        last_index = member_indexes[-1]

        first_index_modified = first_index - 1
        last_index_modified = last_index + 1
        
        no_left_extension = False
        no_right_extension = False

        if first_index_modified < 0:
            no_left_extension = True

        # if last_index_modified is larger than
        # available indices
        if last_index_modified > vals_len - 1:
            no_right_extension = True


        new_left_bound = interval.minval
        new_right_bound = interval.maxval

        if not no_left_extension:
            new_left_bound = vals[first_index_modified]

        if not no_right_extension:
            new_right_bound = vals[last_index_modified]


        # prepare return values
        extensions = []

        if not no_left_extension:
            # when values are [1, 2, 3, 3, 4, 5]
            # and the corresponding interval is (2, 4)
            # instead of resulting interval being (1, 4)
            
            temp_interval = Interval(
                new_left_bound,
                interval.maxval,
                True,
                interval.right_inclusive
            )

            extensions.append((attribute, temp_interval))

        if not no_right_extension:

            temp_interval = Interval(
                interval.minval,
                new_right_bound,
                interval.left_inclusive,
                True
            )

            extensions.append((attribute, temp_interval))

        return extensions
        
    
    # make private
    def get_beam_extensions(self, rule):
        if not rule.was_extended:
            return None

        # literal which extended the rule
        literal = rule.extended_literal
        
        extended_literal = self.__get_direct_extensions(literal)
        
        if not extended_literal:
            return None
        
        copied_rule = rule.copy()
        
        literal_index = copied_rule.antecedent.index(literal)
        
        # so that literal is not an array
        copied_rule.antecedent[literal_index] = extended_literal[0]
        copied_rule.was_extended = True
        copied_rule.extended_literal = extended_literal[0]
        
        return copied_rule

    
    
    def __crisp_accept(self, delta_confidence, delta_support, min_improvement):
        if delta_confidence >= min_improvement and delta_support > 0:
            return True
        else:
            return False
    
    def __conditional_accept(self, delta_conf, min_improvement):
        if delta_conf >= min_improvement:
            return True
        
        