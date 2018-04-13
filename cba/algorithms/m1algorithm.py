import collections
from .rule_algorithm import RuleBuilderAlgorithm
from .classifier import Classifier

import time

class M1Algorithm(RuleBuilderAlgorithm):
    """ M1 Algorithm implementation for CBA 
    Classifier Builder

    Parameters
    ----------


    Attributes
    ----------



    """
    
    def build(self):
        classifier = []
        self.rules.sort(reverse=True)
        dataset = set(self.dataset)
        dataset_len = len(dataset)
        dataset_len_updated = dataset_len
        
        default_classes = []
        default_classes_errors = []
        rule_errors = []
        total_errors = []    

        for rule in self.rules:
            if (dataset_len_updated <= 0):
                break
            
            temp = set()
            temp_len = 0
            temp_satisfies_conseq_cnt = 0
            
            
            for datacase in dataset:
                if rule.antecedent <= datacase:
                    temp.add(datacase)
                    temp_len += 1

                    if rule.consequent == datacase.class_val:  
                        temp_satisfies_conseq_cnt += 1
                        rule.marked = True
                        

            if rule.marked:

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
                
                
                # number of errors the rule will make => all_satisfying - conseq_satisfying
                rule_errors.append(temp_len - temp_satisfies_conseq_cnt)
                
                
                dflt_class_err = dataset_len_updated - most_common_cnt
                err_cnt = dflt_class_err
                    
                
                
                default_classes_errors.append(err_cnt)
                
                total_errors.append(err_cnt + sum(rule_errors))
                
                
                
            temp = set()
            temp_len = 0
            temp_satisfies_conseq_cnt = 0
            
            
        min_errors = min(total_errors)
        
        indices_to_cut = [ i for i in range(len(total_errors)) if total_errors[i] == min_errors ]
        
        idx_to_cut = indices_to_cut[0]
        
        classif = classifier[:idx_to_cut+1]
        default_class = default_classes[idx_to_cut]        
        
        clf = Classifier()
        clf.rules = classif
        clf.default_class = default_class
        

        return clf