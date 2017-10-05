from itertools import chain
from itertools import combinations
from itertools import permutations

from typing import Dict, List, Set, FrozenSet, Tuple

from copy import copy
import itertools
from operator import add
import operator
from functools import reduce


from CBArule import CBArule, M2Rule
from CBAruleGenerator import CBAruleGenerator
from RuleAlgorithms import M1Algorithm, M2Algorithm
from CBAClassifier import CBAClassifier

Item = Tuple[str, int]
ClassItem = Item
Datacase = List[Item]
Dataset = List[Datacase]
YLabels = List[ClassItem]
CondSet = FrozenSet[Item]
CondsupCounts = int
RulesupCounts = Dict[str, int]
ClassLabel = int


class CBA:
    
    def __init__(self, minsup: float, minconf: float):
        self.minsup = minsup
        self.minconf = minconf
        
    def fit(self, dataset: Dataset, Y, algorithm="M1"):
        self.dataset = dataset
        self.Y = Y
        
        self.ruleGenerator = CBAruleGenerator(self.dataset, self.Y, self.minsup, self.minconf)
        rules = self.ruleGenerator.generate()
        args = [rules, self.dataset, self.Y]
        
        self.ruleBuilderAlgorithm = M1Algorithm(*args) if algorithm == "M1" else M2Algorithm(*args)
        self.classifier = self.ruleBuilderAlgorithm.build()
        
    def list_all_rules(self):
        return self.ruleGenerator.cba
        
    def list_classifier_rules(self):
        return self.classifier.rules
        
    def predict(self, x: CondSet):
        return self.classifier.predict(x)
        
        
        
