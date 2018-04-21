import collections

class ClassAssocationRule():
    """ClassAssociationRule (CAR) is defined by its antecedent, consequent,
    support, confidence and id. 

    It has a set of Items in its antecedent and one Item in its
    Consequent. 

    __lt__ and __gt__ operators are overriden so that list of CARs can
    be sorted.  
    
    
    Parameters
    ----------
    
    antecedent: Antecedent
        Items that a Transaction has to satisfy
   
    consequent: Consequent
        Target class of a Transaction that satisfies
        antecedent
    
    support: float
        how many transactions satisfy the rule, relatively
    
    confidence: float
        relative degree of certainty that consequent holds
        given antecedent



    Attributes
    ----------
    antecedent

    conseqent

    support

    confidence

    rid: int
        rule id

    support_count: int
        absolute support count

    marked: bool

    class_cases_covered: collections.Counter
        counter for determining which transactions are
        covered by the antecedent. Important for M2Algorithm.
    
    replace: set of ClassAssociationRule
        set of rules that have higher precedence than
        this rule and can replace it in M2Algorithm.


    """

    id = 0

    def __init__(self, antecedent, consequent, support, confidence):
        self.antecedent = antecedent
        self.consequent = consequent
        self.support = support
        self.confidence = confidence
        self.rulelen = len(antecedent) + 1
        self.rid = ClassAssocationRule.id

        ClassAssocationRule.id += 1

        self.support_count = 0
        
        self.marked = False
        
        self.class_cases_covered = collections.Counter()
        self.replace = set()
        
        
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
    
    def __len__(self):
        """
        returns
        -------
        
        length of this rule 
        """
        return len(self.antecedent) + len(self.consequent)


    def __repr__(self):
        args = [self.antecedent.string(), "{" + self.consequent.string() + "}", self.support, self.confidence, self.rulelen, self.rid]
        text = "CAR {} => {} sup: {:.2f} conf: {:.2f} len: {}, id: {}".format(*args)

        return text