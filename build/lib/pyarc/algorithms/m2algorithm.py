from .rule_algorithm import RuleBuilderAlgorithm
from .classifier import Classifier
from ..data_structures import ClassAssocationRule, Antecedent, Consequent

import random

import collections

class M2Algorithm(RuleBuilderAlgorithm):
    """
    Implementation of M2 Algorithm for CBA.
    """
    
    def build(self):

        self.rules.sort(reverse=True)
        
        self.dataset_frozen = self.dataset
        self.dataset_len = len(self.dataset_frozen)

        # set of crules that have higher precedence
        # that their corresponding wrules
        self.Q = set()
        
        # set of all crules
        self.U = set()
        
        # set of conflicting rules
        self.A = set()
        
        self.classifier = []
        
        self.stage1()
        self.stage2()
        self.stage3()
        
        clf = Classifier()
        clf.rules = self.classifier
        clf.default_class = self.default_class
        self.calculate_default_class_properties(clf)
        
        return clf
    
        
    def stage1(self):
        for datacase in self.dataset_frozen:
            # finds the highest precedence crules and wrules
            crule, wrule = self.maxcoverrule(datacase, self.rules)
        
            if crule is None:
                crule = self.emptyrule()
                
            if wrule is None:
                wrule = self.emptyrule()
                
            self.U.add(crule)
            
            crule.class_cases_covered.update([datacase.class_val.value])
            
            if crule > wrule:
                self.Q.add(crule)
                crule.marked = True
            else:
                structure = (datacase, datacase.class_val.value, crule, wrule)
                self.A.add(structure)
                
            
                
    
    def stage2(self):
        
        for conflicting_struct in self.A:
            datacase, clazz, crule, wrule = conflicting_struct
            
            
            if wrule.marked:
                crule.class_cases_covered[clazz] -= 1
                wrule.class_cases_covered[clazz] += 1
            
            else:
                wset = self.allcover_rules(self.U, datacase, crule)
                for w in wset:
                    w.replace.add((crule, datacase, clazz))
                    w.class_cases_covered[clazz] += 1
                    
                self.Q = self.Q.union(wset)
        
        
    def stage3(self):
        Qlist = sorted(self.Q, reverse=True)

        rule_errors = 0
        rule_supcount = 0
        total_errors_list = []
        default_classes_list = []
        rules_list = []
        
        # class distribution
        classdist = collections.Counter(map(lambda d: d.class_val.value, self.dataset_frozen))
        classdist_keys = list(classdist.keys())
        
        for rule in Qlist:
            if rule.class_cases_covered[rule.consequent.value] > 0:
                for (rule_replace, dcase, clazz) in rule.replace:
                    if dcase.alreadycovered == True:
                        rule.class_cases_covered[clazz] -= 1
                    else:
                        dcase.alreadycovered = True
                        rule_replace.class_cases_covered[clazz] -= 1
                
                rule_errors += self.errors_of_rule(rule)
                rule_supcount += rule.support_count
                
                classdist = self.update_class_distr(classdist, rule)
                
                default_class = self.select_default_class(classdist)
                default_class_count = default_class[1]
                default_class_label = default_class[0]
                
                default_errors = self.dataset_len - rule_supcount - default_class_count
                
                total_errors = rule_errors + default_errors
                
                rules_list.append(rule)
                default_classes_list.append(default_class_label)
                total_errors_list.append(total_errors)
                
        
        if len(total_errors_list) != 0:
            min_value = min(total_errors_list)
            
            min_indices = [ idx for (idx, err_num) in enumerate(total_errors_list) if err_num == min_value ]
            min_idx = min_indices[0]
            
            final_classifier = [ rule for rule in rules_list[:min_idx + 1] ]
            default_class = default_classes_list[min_idx]

            if not default_class:
                i = min_idx
                while not default_class:
                    i -= 1
                    default_class = default_classes_list[i]

            self.classifier = final_classifier
            self.default_class = default_class
            self.default_class_attribute = classdist_keys[0][0]
        else:
            possible_default_classes = list(classdist)
            random_class_idx = random.randrange(0, len(possible_default_classes))
            default_class_att, default_class_value = list(classdist.keys())[random_class_idx]

            self.classifier = []
            self.default_class = default_class_value
            self.default_class_attribute = default_class_att
    
    def emptyrule(self):
        """returns rule with empty antecedent
        and consequent
        """
        return ClassAssocationRule(Antecedent([]), Consequent(None, None), 0, 0)
    
    
    def maxcoverrule(self, datacase, rules):
        """
        finds the highest precedence rule that covers
        the case d
        
        
        Arguments
        ---------
        rules: sorted rules
            
        datacase: instance d
            
        """
        crule, wrule = None, None
        
        
        for rule in rules:
            if rule.antecedent <= datacase:
                if rule.consequent == datacase.class_val and not crule:
                    # save cRule
                    crule = rule
                    if crule and wrule:
                        return crule, wrule
                elif rule.consequent != datacase.class_val and not wrule:
                    # save wRule
                    wrule = rule
                    if crule and wrule:
                        return crule, wrule

        
        
        return crule, wrule
    
    
    def allcover_rules(self, U, datacase, crule):
        """method for finding all rules from a set U
        that cover datacase and have a higher precedence
        tha crule
        """
        wset = set()
        
        for replacingrule in U:
            if replacingrule > crule and replacingrule.antecedent <= datacase and replacingrule.consequent.value != datacase.class_val.value:
                wset.add(replacingrule)
        
        return wset
    
    def errors_of_rule(self, rule):
        """method for computing errors of
        a rule
        """
        rule.support_count = sum(rule.class_cases_covered.values()) 
        return rule.support_count - rule.class_cases_covered[rule.consequent.value]
    
    
    
    def select_default_class(self, classdist):
        """method for selecting default class
        from class distribution
        """
        most_common = classdist.most_common(1)
        
        if not most_common:
            return (None, 0)
        
        return most_common[0]
    
