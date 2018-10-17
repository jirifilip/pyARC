from .algorithms import M1Algorithm, M2Algorithm, generateCARs
from .data_structures import TransactionDB

class CBA():
    """Class for training a testing the
    CBA Algorithm.

    Parameters:
    -----------
    support : float
    confidence : float
    algorithm : string
        Algorithm for building a classifier.
    maxlen : int
        maximum length of mined rules
    """


    def __init__(self, support=0.10, confidence=0.5, maxlen=10, algorithm="m1"):
        if algorithm not in ["m1", "m2"]:
            raise Exception("algorithm parameter must be either 'm1' or 'm2'")
        if 0 > support or support > 1:
            raise Exception("support must be on the interval <0;1>")
        if 0 > confidence or confidence > 1:
            raise Exception("confidence must be on the interval <0;1>")
        if maxlen < 1:
            raise Exception("maxlen cannot be negative or 0")
        
        self.support = support * 100
        self.confidence = confidence * 100
        self.algorithm = algorithm
        self.maxlen = maxlen
        self.clf = None
        
        self.available_algorithms = {
            "m1": M1Algorithm,
            "m2": M2Algorithm
        }

        
        


    def rule_model_accuracy(self, txns):
        """Takes a TransactionDB and outputs
        accuracy of the classifier
        """
        if not self.clf:
            raise Exception("CBA must be trained using fit method first")
        if not isinstance(txns, TransactionDB):
            raise Exception("txns must be of type TransactionDB")

        return self.clf.test_transactions(txns)
        
    def fit(self, transactions):
        """Trains the model based on input transaction
        and returns self.
        """
        if not isinstance(transactions, TransactionDB):
            raise Exception("transactions must be of type TransactionDB")

        used_algorithm = self.available_algorithms[self.algorithm]
        
        cars = generateCARs(transactions, support=self.support, confidence=self.confidence, maxlen=self.maxlen)

        self.clf = used_algorithm(cars, transactions).build()
        
        return self
    
    def predict(self, X):
        """Method that can be used for predicting
        classes of unseen cases.

        CBA.fit must be used before predicting.
        """
        if not self.clf:
            raise Exception("CBA must be train using fit method first")

        if not isinstance(X, TransactionDB):
            raise Exception("X must be of type TransactionDB")


        return self.clf.predict_all(X)
    
    
    

