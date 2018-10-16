import re
import numpy as np


def make_intervalfunc(minv, maxv, left_inclusivity, right_inclusivity):
    def inner_func(value):
        if greaterthan(value, minv, left_inclusivity) and lesserthan(value, maxv, right_inclusivity):
            return True
        else:
            return False
        
    return inner_func
        
def greaterthan(a, b, inclusivity):
    if inclusivity:
        if a >= b: return True
    elif a > b: return True
    
    return False
        
def lesserthan(a, b, inclusivity):
    if inclusivity:
        if a <= b: return True
    elif a < b: return True
    
    return False


class Interval:

    def __init__(self, minval, maxval, left_inclusive, right_inclusive):
        self.minval = minval
        self.maxval = maxval
        self.left_inclusive = left_inclusive
        self.right_inclusive = right_inclusive
        
        
        self.left_bracket = "<" if left_inclusive else "("
        self.right_bracket = ">" if right_inclusive else ")"
        
        self.__membership_func = np.vectorize(
            make_intervalfunc(self.minval, self.maxval, self.left_inclusive, self.right_inclusive)
        )
            
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
            
    def refit(self, vals):
        """refit values to a finer grid
        """
        values = np.array(vals)
        
        mask = self.test_membership(values)
        new_array = values[mask]

        left, right = min(new_array), max(new_array)

        return Interval(left, right, True, True)
        
            
    def test_membership(self, value):
        return self.__membership_func(value)
    
    def isin(self, value):
        return self.test_membership([value])[0]

    def overlaps_with(self, other):
        return self.isin(other.minval) or self.isin(other.maxval)
        

    def string(self):
        return "{}{};{}{}".format(self.left_bracket, self.minval, self.maxval, self.right_bracket)
        
    def __repr__(self):
        return "Interval[{}{};{}{}]".format(self.left_bracket, self.minval, self.maxval, self.right_bracket)