from collections import Counter

from ..data_structures import ClassAssocationRule, Antecedent, Consequent

class RuleBuilderAlgorithm:
    """Common ancestor for M1 and M2 Algorithms
    to provide common interface.
    """

    def __init__(self, rules, dataset):
        self.rules = rules
        self.dataset = dataset
        self.y = dataset.class_labels
        
    def update_class_distr(self, classdist, rule):
        return classdist - rule.class_cases_covered

    def calculate_default_class_properties(self, clf):
        """This function is used for calculating
        default class support and confidence
        """
        default_class = clf.default_class
        class_distribution = Counter([ value for _, value in self.y])

        clf.default_class_support = class_distribution[default_class] / len(self.y)
        clf.default_class_confidence = class_distribution[default_class] / len(self.y)

        default_rule_ant = Antecedent({})
        default_rule_conseq = Consequent(clf.default_class_attribute, clf.default_class)

        clf.default_rule = ClassAssocationRule(
            default_rule_ant,
            default_rule_conseq,
            clf.default_class_support,
            clf.default_class_confidence
        )

    