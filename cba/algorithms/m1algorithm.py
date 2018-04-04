import collections
from .rule_algorithm import RuleBuilderAlgorithm
from .classifier import Classifier

import time

class M1Algorithm(RuleBuilderAlgorithm):
    
    def build(self):
        classifier = []
        self.rules.sort(reverse=True)
        dataset = set(self.dataset)
        dataset_len = len(dataset)
        dataset_len_updated = dataset_len
        
        default_classes = []
        default_classes_errors = []
        satisfies_ant_count = []
        rule_errors = []
        rule_right = []
        total_errors = []    

        for rule in self.rules:
            if (dataset_len_updated <= 0):
                break
            
            temp = set()
            temp_len = 0
            temp_satisfies_ant_cnt = 0
            
            
            for datacase in dataset:
                
                if rule.antecedent <= datacase: # or set(dict(rule.antecedent)) == set(dict(datacase.items)):
                    temp_satisfies_ant_cnt += 1
                    
                    if rule.consequent == datacase.class_val:  
                        
                        temp.add(datacase)
                        temp_len += 1
                        rule.marked = True
                        
            if rule.marked == True:
                classifier.append(rule)
                
                dataset -= temp
                dataset_len_updated -= temp_len
                
                
                ctr = collections.Counter(map(lambda d: d.class_val.value, dataset))
                
                # this will be the default class
                most_common_tuple = ctr.most_common(1)
                
                most_common_cnt = 0
                most_common_label = "None"
                
                try:
                    most_common_tuple = most_common_tuple[0]
                    most_common_cnt = most_common_tuple[1]
                    most_common_label = most_common_tuple[0]
                except IndexError:
                    pass
                
                    
                
                # this is the default class label inserted at corresponding list
                default_classes.append(most_common_label)
                
                # number of datacases that satisfy the rule
                satisfies_ant_count.append(temp_satisfies_ant_cnt)
                
                # number of errors the rule will make => all_satisfying - conseq_satisfying
                rule_errors.append(temp_satisfies_ant_cnt - temp_len)
                rule_right.append(temp_len)
                
                
                #dflt_class_err = dataset_len - (sum(satisfies_ant_count) + most_common_tuple[1])
                dflt_class_err = dataset_len_updated - most_common_cnt
                err_cnt = dflt_class_err
                #if dflt_class_err > 0: err_cnt = dflt_class_err
                    
                
                
                default_classes_errors.append(err_cnt)
                
                total_errors.append(err_cnt + sum(rule_errors))
                
                
                
            temp = set()
            temp_len = 0
            temp_satisfies_ant_cnt = 0
            
            
        min_errors = min(total_errors)
        
        indices_to_cut = [ i for i in range(len(total_errors)) if total_errors[i] == min_errors ]
        
        idx_to_cut = indices_to_cut[-1]
        
        classif = classifier[:idx_to_cut+1]
        default_class = default_classes[idx_to_cut]        
        
        #return classifier, default_classes, total_errors, rule_errors, satisfies_ant_count, rule_right, default_classes_errors
        
        clf = Classifier()
        clf.rules = classif
        clf.default_class = default_class
        

        return clf