
import copy

from .interval_reader import IntervalReader
from .quant_dataset import QuantitativeDataFrame

class QuantitativeCAR:
    
    interval_reader = IntervalReader()
    
    def __init__(self, rule):
        self.antecedent = self.__create_intervals_from_antecedent(rule.antecedent)
        self.consequent = copy.copy(rule.consequent)
        
        self.confidence = rule.confidence
        self.support = rule.support
        self.rulelen = rule.rulelen
        self.rid = rule.rid
        
        # property which indicates wheter the rule was extended or not
        self.was_extended = False
        # literal which extended the rule
        self.extension_literal = None

        self.interval_reader = QuantitativeCAR.interval_reader
        
        
    def __create_intervals_from_antecedent(self, antecedent):
        interval_antecedent = []
        
        for literal in antecedent:
            attribute, value = literal
            
            interval = self.interval_reader.read(value)
            
            interval_antecedent.append((attribute, interval))
        
        
        return self.__sort_antecedent(interval_antecedent)
    
    
    def __sort_antecedent(self, antecedent):
        return sorted(antecedent)
    
    
    def update_properties(self, quant_dataframe):
        """updates rule properties using instance
        of QuantitativeDataFrame
        
        properties:
            support, confidence, rulelen
        
        """
        
        if quant_dataframe.__class__.__name__ != "QuantitativeDataFrame":
            raise Exception(
                "type of quant_dataframe must be QuantitativeDataFrame"
            )
            
        
        support, confidence = quant_dataframe.calculate_rule_statistics(self)
        
        self.support = support
        self.confidence = confidence
        # length of antecedent + length of consequent
        self.rulelen = len(self.antecedent) + 1
        
    
    def copy(self):
        return copy.deepcopy(self)


    def __deepcopy__(self, memo):

        copied = copy.copy(self)
        copied.antecedent = copy.deepcopy(self.antecedent)
        copied.consequent = copy.deepcopy(self.consequent)

        return copied
        
        
    def __repr__(self):
        ant = self.antecedent
        ant_string_arr = [ key + "=" + val.string() for key, val in ant ]
        ant_string = "{" + ",".join(ant_string_arr) + "}"
        
        args = [
            ant_string,
            "{" + self.consequent.string() + "}",
            self.support,
            self.confidence,
            self.rulelen,
            self.rid
        ]
        
        text = "CAR {} => {} sup: {:.2f} conf: {:.2f} len: {}, id: {}".format(*args)

        return text
    
    
    def __gt__(self, other):
        """
        precedence operator. Determines if this rule
        has higher precedence. Rules are sorted according
        to their confidence, support, length and id.
        """
        if (self.confidence > other.confidence):
            return True
        elif (self.confidence == other.confidence and
              self.support > other.support):
            return True
        elif (self.confidence == other.confidence and
              self.support == other.support and
              self.rulelen < other.rulelen):
            return True
        elif(self.confidence == other.confidence and
              self.support == other.support and
              self.rulelen == other.rulelen and
              self.rid < other.rid):
            return True
        else:
            return False
        
    
    def __lt__(self, other):
        """
        rule precedence operator
        """
        return not self > other
    
    
    def __eq__(self, other):
        return self.rid == other.rid
