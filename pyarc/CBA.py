from .algorithms import M1Algorithm, M2Algorithm, generateCARs
import time

class CBA():
    def __init__(self, support=0.10, confidence=0.5, algorithm="m1"):
        self.support = support * 100
        self.confidence = confidence * 100
        self.algorithm = algorithm
        
        self.available_algorithms = {
            "m1": M1Algorithm,
            "m2": M2Algorithm
        }

    def rule_model_accuracy(self, txns):
        return self.clf.test_transactions(txns)
        
    def fit(self, transactions):
        used_algorithm = self.available_algorithms[self.algorithm]
        
        cars = generateCARs(transactions, support=self.support, confidence=self.confidence)


        self.clf = used_algorithm(cars, transactions).build()
        
        return self
    
    def predict(self, X):
        return self.clf.predict_all(X)
    
    
    

