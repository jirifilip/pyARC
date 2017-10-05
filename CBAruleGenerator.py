from CBArule import CBArule

from itertools import chain
from itertools import combinations
from itertools import permutations

from typing import Dict, List, Set, FrozenSet, Tuple

from copy import copy
import itertools
from operator import add
import operator
from functools import reduce


class CBAruleGenerator:
    
    def __init__(self, dataset, Y, minsup: int, minconf: int):
        self.dataset = dataset
        self.Y = Y
        self.minsup = minsup
        self.minconf = minconf
        self.frequent_ruleitems = None
        
    def generate_unique_items(self, items, k = 1):
        """
        generates unique items from dataset of length k
        """
        
        if k > 1:
            items = combinations(items, k)

        unique_k_items = []

        for item in items:
            if k == 1:
                item = [item]
            else:
                item = chain(*item)
            temporary_set = frozenset(item)
            length = len(list(temporary_set))
            if temporary_set not in unique_k_items and length == k:
                unique_k_items.append(temporary_set)
            
        return unique_k_items
    
        
    def determine_frequent_itemsets(self, itemsets, dataset, y):
        freq_itemsets = {}
        for i, datacase in enumerate(dataset):
            for itemset in itemsets:
                freq_itemsets.setdefault(itemset, {
                    "condsupCount": 0,
                    "rulesupCount": {}
                })
                
                if itemset <= datacase:
                    freq_itemsets[itemset]["condsupCount"] += 1
                    _, class_name = y[i] 
                    freq_itemsets[itemset]["rulesupCount"].setdefault(class_name, 0)
                    freq_itemsets[itemset]["rulesupCount"][class_name] += 1
                    
                
        return freq_itemsets
    
    
    def choose_correct_class(self, frequent_items):
        """
        todo: random choice
        """

        for freq_item in frequent_items:
            item = frequent_items[freq_item]

            max_class = (None, 0)
            for class_name, rulesupCount in item["rulesupCount"].items():
                k, v = max_class
                if rulesupCount > v:
                    max_class = (class_name, rulesupCount)

            item["rulesupCount"] = max_class

        return frequent_items
    
    def filter_rules(self, rules, minsup, minconf, dataset_len):
        new_rules = {}

        for rule, y in rules.items():
            condsupCount = y["condsupCount"]
            class_name, rulesupCount = y["rulesupCount"]

            confidence = 0 if condsupCount == 0 else rulesupCount / condsupCount * 100
            support = rulesupCount / dataset_len * 100

            if support >= minsup and confidence >= minconf and class_name is not None:
                new_rules[rule] = y

        return new_rules
    
    
    def generate_frequent_ruleitems(self):
        """
        generates frequent ruleitems
        """
        
        candidates = []
        frequent_ruleitems = []
        cba = []
        dataset = self.dataset
        dataset_len = len(dataset)
        y = copy(self.Y)

        frozen_dataset = map(frozenset,dataset)

        candidate = self.generate_unique_items(chain(*dataset))
        candidate_rules = self.determine_frequent_itemsets(candidate, frozen_dataset, y)
        correct_class_rules = self.choose_correct_class(candidate_rules)
        filtered_rules = self.filter_rules(correct_class_rules, self.minsup, self.minconf, dataset_len)
        frequent_ruleitems.append(filtered_rules)
        candidates.append(list(filtered_rules.keys()))

        k = 1
        while frequent_ruleitems[k - 1]:
            frozen_dataset = map(frozenset, dataset)
            candidate = self.generate_unique_items(map(list, candidates[k - 1]), k + 1)
            candidate_rules = self.determine_frequent_itemsets(candidate, frozen_dataset, y)
            correct_class_rules = self.choose_correct_class(candidate_rules)
            filtered_rules = self.filter_rules(correct_class_rules, self.minsup, self.minconf, dataset_len)
            frequent_ruleitems.append(filtered_rules)
            candidates.append(list(filtered_rules.keys()))

            k += 1

        return frequent_ruleitems
    
    
    def generate(self):
        freq = self.generate_frequent_ruleitems()
        cba = []
        dataset_len = len(self.dataset)
        for ruleset in freq:
            for rule, y in ruleset.items():
                cba.append(CBArule(rule, y, dataset_len))

        cba.sort(reverse=True)

        self.cba = cba
        return self.cba