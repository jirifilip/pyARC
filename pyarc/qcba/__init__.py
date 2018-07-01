from ..data_structures import ClassAssocationRule
from .interval import Interval

class QuantClassAssociationRule:
    
    def __init__(self, rule):
        
        if type(rule) != ClassAssocationRule:
            raise Exception("Type of rule must be: ClassAssocationRule")
        
        self.rule = rule
    
        antecedent_string = rule.antecedent
        
        self.new_antecedent = []
        
        for item in antecedent_string:
            attr, val = item
            
            interval = Interval(val)
            
            self.new_antecedent.append((attr, interval))


        
    def __repr__(self):
        r = self.rule
        
        ant = self.new_antecedent
        ant_string_arr = [ key + "=" + val.string() for key, val in ant ]
        ant_string = "{" + ",".join(ant_string_arr) + "}"
        
        
        args = [ant_string, "{" + r.consequent.string() + "}", r.support, r.confidence, r.rulelen, r.rid]
        text = "CAR {} => {} sup: {:.2f} conf: {:.2f} len: {}, id: {}".format(*args)

        return text