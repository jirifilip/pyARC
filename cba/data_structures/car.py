import collections

class ClassAssocationRule():
    def __init__(self, antecedent, consequent, support, confidence):
        self.antecedent = antecedent
        self.consequent = consequent
        self.support = support
        self.confidence = confidence
        self.rulelen = len(antecedent)
        
        self.support_count = 0
        
        self.marked = False
        
        self.class_cases_covered = collections.Counter()
        self.replace = set()
        
        
        self.error_number = 0
    
    def __gt__(self, other):
        """
        precedence operator
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
        else:
            return False
    
    def __lt__(self, other):
        """
        rule precedence operator
        """
        return not self > other
    
    def __len__(self):
        return len(self.antecedent) + len(self.consequent)
    
    def __repr__(self):
        args = [self.antecedent, self.consequent, self.support, self.confidence, self.rulelen]
        text = "CAR {0} -> {1} | support: {2:.2f}, confidence: {3:.2f}, len: {4}".format(*args)
        return text