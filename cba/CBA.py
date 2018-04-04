from .algorithms import M1Algorithm, M2Algorithm, generateCARs
import time

class CBA():
    def __init__(self, support=0.01, confidence=0.5, algorithm="m1"):
        self.support = support * 100
        self.confidence = confidence * 100
        self.algorithm = algorithm
        
        self.available_algorithms = {
            "m1": M1Algorithm,
            "m2": M2Algorithm
        }
        
    def fit(self, transactions):
        
        used_algorithm = self.available_algorithms[self.algorithm]
        
        generating_time1 = time.time()
        cars = generateCARs(transactions, support=self.support, confidence=self.confidence)
        generating_duration = time.time() - generating_time1


        self.clf = used_algorithm(cars, transactions).build()
        
        # Return the classifier
        return self
    
    def predict(self, X):

        return self.clf.predict_all(X)
    
    
    

