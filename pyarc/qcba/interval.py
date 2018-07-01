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

    interval_regex = re.compile("(<|\()(\d+);(\d+)(\)|>)")
    
    def __init__(self, interval_string="<0;0)"):
        try:
            args = Interval.interval_regex.findall(interval_string)[0]
            self.left_bracket, self.minval, self.maxval, self.right_bracket = args
            
            self.left_inclusive = True if self.left_bracket == "<" else False
            self.right_inclusive = True if self.right_bracket == ">" else False
            
            self.minval, self.maxval = float(self.minval), float(self.maxval)
            
            self.__membership_func = np.vectorize(
                make_intervalfunc(self.minval, self.maxval, self.left_inclusive, self.right_inclusive)
            )
            
        except Exception as e:
            raise e
            
    @classmethod        
    def from_scalars(clazz, minval, maxval, left_inc, right_inc):
        """rework this as the default constructor
        """
        interval_string = "{}{};{}{}".format(
            "<" if left_inc else "(",
            minval,
            maxval,
            ">" if right_inc else ")"
        )
        
        return clazz(interval_string)
    
    def __hash__(self):
        return hash(repr(self))
            
    def refit(self, vals):
        """refit values to grid
        """
        values = np.array(vals)
        
        mask = self.test_membership(values)
        new_array = values[mask]

        left, right = min(new_array), max(new_array)

        return Interval.from_scalars(left, right, True, True)
        
            
    def test_membership(self, value):
        return self.__membership_func(value)
        

    def string(self):
        return "{}{};{}{}".format(self.left_bracket, self.minval, self.maxval, self.right_bracket)
        
    def __repr__(self):
        return "Interval[{}{};{}{}]".format(self.left_bracket, self.minval, self.maxval, self.right_bracket)