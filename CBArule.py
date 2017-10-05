class CBArule:
    rule_id = 0
    
    def __init__(self, condset, supcounts, dataset_len):
        self.id = CBArule.rule_id
        CBArule.rule_id += 1
        self.condset = frozenset(condset)
        self.supcounts = supcounts
        self.dataset_len = dataset_len
        self.condsupCount = supcounts["condsupCount"]
        self.y, self.rulesupCount = supcounts["rulesupCount"]
        self.marked = False
        self.error_number = 0
        
        self.confidence = self.rulesupCount / self.condsupCount * 100
        self.support = self.rulesupCount / dataset_len * 100
        
    def mark(self):
        self.marked = True
        
    def is_marked(self):
        return self.marked
    
    def test_datacase(self, datacase, y):
        condset_test = self.condset <= datacase
        y_test = self.y == y
        return condset_test and y_test
    
    def mark_for_m2(self):
        self.class_cases_covered = 0
    
    def convert_to_m2_rule(self):
        return M2Rule(self.condset, self.supcounts, self.dataset_len)
    
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
              self.support > other.support and
              self.rule_id < other.rule_id):
            return True
        else:
            return False
        
    def __lt__(self, other):
        return not self.__gt__(other)
    
    def __repr__(self):
        txt = ", ".join(map(repr, self.condset))
        txt += " -> {0}".format(self.y)
        txt = "CBA rule {0} | errors: {1} | confidence: {2:.2f}% | support: {3:.2f}% | id: {4}".format(
            txt, self.error_number, self.confidence, self.support, self.id
        )
        return txt
    
    
class M2Rule(CBArule):
    
    def __init__(self, condset, supcounts, dataset_len):
        CBArule.__init__(self, condset, supcounts, dataset_len)
        self.class_cases_covered = 0
        self.replace