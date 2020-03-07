import collections
from .rule_algorithm import RuleBuilderAlgorithm
from .classifier import Classifier

import time
import random

class M1Algorithm(RuleBuilderAlgorithm):
    """ M1 Algorithm implementation.
    """
    
    def build(self):
        
        # list for storing rules to be used in the classifier
        classifier = []
        # list for storing default classes associated
        # with rules in the classifier
        default_classes = []
        # list for storing errors of said default classes
        default_classes_errors = []
        # list for storing rule errors from classifier
        rule_errors = []
        # list for storing total errors
        # (rule_errors + default_classes_errors)
        total_errors = []
        # class distribution
        # for calculating the default's rule confidence
        # and support
        class_distribution = collections.Counter(self.y)
        classdist_keys = list(class_distribution.keys())


        # sorting rules based on the precedence operator
        self.rules.sort(reverse=True)

        # converting TransactionDB to a set
        # so that set intersection and difference can be used
        dataset = set(self.dataset)

        # obtaining the set's length. We do this only once to
        # save processing time.
        # this is a constant variable
        dataset_len = len(dataset)

        # When we want to update the dataset_len, we use
        # this variable. Length is updated by subtracting 
        # absolute support of a rule from it
        dataset_len_updated = dataset_len
        
        

        for rule in self.rules:
            # if all data cases have been covered
            # break the loop to save time
            if (dataset_len_updated <= 0):
                break
            

            # temp serves for storing datacases
            # that have been covered by current rule
            temp = set()
            # temp len is for determining temp's length
            # without using len(temp) to save time
            temp_len = 0
            # number of rule that satisfy both antecedent
            # and consequent of the current rule
            temp_satisfies_conseq_cnt = 0
            
            
            for datacase in dataset:
                # if datacase satisfies rule's antecedent
                # we'll store it in temp and increment
                #  temp's len
                if rule.antecedent <= datacase:
                    temp.add(datacase)
                    temp_len += 1

                    # we'll mark the rule if datacase
                    # satisfies its consequent. And increment
                    # the counter
                    if rule.consequent == datacase.class_val:  
                        temp_satisfies_conseq_cnt += 1
                        rule.marked = True
                        

            # if rule satisfied at least one consequent
            if rule.marked:
                classifier.append(rule)

                # we subtract already covered rules
                # from dataset                
                dataset -= temp
                # and update dataset's length
                dataset_len_updated -= temp_len
                
                # we'll obtain Counter of remaining class values
                # in the dataset using map to save time
                class_distribution = collections.Counter(map(lambda d: d.class_val.value, dataset))
                
                # the most common value from the counter will be
                # the default class
                most_common_tuple = class_distribution.most_common(1)
                

                # here we'll do some checking in case
                # the counter is empty
                most_common_cnt = 0
                most_common_label = "None"
                
                try:
                    most_common_tuple = most_common_tuple[0]
                    most_common_cnt = most_common_tuple[1]
                    most_common_label = most_common_tuple[0]
                except IndexError:
                    pass
                
                    
                # the most common label will be inserted into 
                # the list                
                default_classes.append(most_common_label)
                
                
                # number of errors the rule will make => 
                #
                # difference of:
                # all transactions that satisfy its antecedent
                # and
                # all transactions that satisfy both antecedent and consequent
                rule_errors.append(temp_len - temp_satisfies_conseq_cnt)
                
                # default errors
                #
                # difference of:
                # length of remaining dataset
                # and
                # count of most common class 
                dflt_class_err = dataset_len_updated - most_common_cnt
                
                
                err_cnt = dflt_class_err
                    
                
                default_classes_errors.append(err_cnt)
                
                total_errors.append(err_cnt + sum(rule_errors))
                
                
        
        # finding the smallest number of errors
        # but checking if at least one rule classified an instance
        if len(total_errors) != 0:            
            min_errors = min(total_errors)
            
            # finding the index of smallest number of errors
            idx_to_cut = total_errors.index(min_errors)
            
            final_classifier = classifier[:idx_to_cut+1]
            default_class = default_classes[idx_to_cut]        
            
            # creating the final classifier
            clf = Classifier()
            clf.rules = final_classifier
            clf.default_class = default_class
            clf.default_class_attribute = classdist_keys[0][0]

        else:
            clf = Classifier()
            clf.rules = []

            possible_default_classes = list(class_distribution)
            random_class_idx = random.randrange(0, len(possible_default_classes))
            default_class_att, default_class_value = classdist_keys[random_class_idx]
            clf.default_class = default_class_value
            clf.default_class_attribute = default_class_att


        self.calculate_default_class_properties(clf)        

        return clf


        