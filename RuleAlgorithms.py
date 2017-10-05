from copy import copy
from CBAClassifier import CBAClassifier
from functools import reduce

class RuleBuilderAlgorithm:
    def __init__(self, rules, dataset, y):
        self.rules = rules
        self.dataset = dataset
        self.y = y
        
    def get_majority_class(self, y):
        unique_keys = {}
        for value in y:
            unique_keys.setdefault(value, 0)
            unique_keys[value] += 1

        maximum = (0, 0)
        for key, value in unique_keys.items():
            class_name, count = maximum
            if count < value:
                maximum = key, value
        
        return maximum[0]
        
        
        
class M1Algorithm(RuleBuilderAlgorithm):
    
    def __init__(self, rules, dataset, y):
        RuleBuilderAlgorithm.__init__(self, rules, dataset, y)
    
    def build(self):
        self.classifier = CBAClassifier()
        sorted_rules = self.rules.sort(reverse=True)

        copied_dataset = list(map(frozenset, copy(self.dataset)))
        copied_y = copy(self.y)

        for rule in self.rules:
            temp = set()
            for datacase_id, datacase in enumerate(copied_dataset):
                _, y_current = copied_y[datacase_id]
                if (rule.test_datacase(datacase, y_current)):
                    temp.add(datacase_id)
                    rule.mark()

            if rule.is_marked():
                self.classifier.add_rule(rule)
                copied_dataset = [datacase for idx, datacase in enumerate(copied_dataset) if idx not in temp]
                copied_y = [dataclass for idx, dataclass in enumerate(copied_y) if idx not in temp]

                default_class = self.get_majority_class(map(lambda n: n[1], self.y))
                self.classifier.add_default_class(default_class)
                self.classifier.test_dataset(map(frozenset, self.dataset), self.y)

        return self.classifier
    
    
class M2Algorithm(RuleBuilderAlgorithm):
    
    def __init__(self, rules, dataset, y):
        RuleBuilderAlgorithm.__init__(self, rules, dataset, y)
        self.c_rules = set() #correct rules
        self.w_rules = set() #wrong rules
        
        self.high_precedence_c_rules = set()
        self.lower_precedence_c_rules = set()
        
    def all_cover_rules(self):
        self.rules.sort(reverse = True)
        
        cover_rules = []
        
        for rule in self.rules:
            if rule <= self.datacase:
                pass
        pass
        
    def max_cover_rule(self, rules, datacase):
        rules.sort(reverse = True)
        for rule in rules:
            if rule <= datacase:
                return rule
        return None
        """
        finds highest precedence rule that covers the case d
        """
    
    def filter_rules_for_class(self, class_name):
        def filter_func(rule):
            if rule.y == class_name:
                return True
            else:
                return False
            
        return filter_func
    
    
    def find_all_rules_for_classes(self):
        distinct_y = list(set(copy(self.y)))
        rules_for_class = {}
        for y in distinct_y:
            rules = list(
                filter(
                    self.filter_rules_for_class(y),
                    self.rules
                )
            )
            rules_for_class[y] = rules
        
        return rules_for_class
    
    def find_c_rule_w_rule(self, rules_for_class, correct_class):
        all_rules = copy(rules_for_class)
        c_rules = rules_for_class[correct_class]
        del all_rules[correct_class]
        w_rules = list(
            reduce(add, all_rules.items())
        )
        return c_rules, w_rules
        
    
    def traverse_dataset(self):
        """
        stage-1
        """
        rules_for_class = self.find_all_rules_for_classes()
        
        
        for idx, datacase in enumerate(dataset):
            all_c_rules, all_w_rules = find_c_rule_w_rule
            
            _, class_label = self.y[idx]
            
            c_rule = self.max_cover_rule(all_c_rules, datacase)
            w_rule = self.max_cover_rule(all_w_rules, datacase)
    
            self.c_rules.add(c_rule)
            
            #class cases cover
            if c_rule > w_rule:
                self.high_precedence_c_rules.add(c_rule)
                c_rule.mark()
            else:
                #INCLUDE CLASS!
                rule = M2RuleDataStructure(
                    datacase.id, class_label, c_rule, w_rule
                )
                self.lower_precedence_c_rules.add(rule)
                
    
    
    def build(self):
        """
        stage-2
        """
        self.traverse_dataset()
        
        for entry in self.lower_precedence_c_rules:
            dataset_id = entry.dataset_id
            y = entry.y
            c_rule = entry.c_rule
            w_rule = entry.w_rule
            
            
            if entry.w_rule.is_marked():
                c_rule.mark_for_m2()
                w_rule.mark_for_m2()
                c_rule.class_cases_covered -= 1
                w_rule.class_cases_covered += 1
            else:
                pass
                
    
    

class M2RuleDataStructure:
    
    def __init__(self, datacase_id, y, c_rule, w_rule):
        self.datacase_id = datacase_id
        self.y = y
        self.c_rule = c_rule
        self.w_rule = w_rule