import re
import numpy as np

from .interval import Interval

class IntervalReader():
    
    
    interval_regex = re.compile("(<|\()(\d+(?:\.(?:\d)+)?);(\d+(?:\.(?:\d)+)?)(\)|>)")
    
    
    def __init__(self):
        # opened interval brackets
        self.__open_bracket = "(", ")"
        
        # closed interval brackets
        self.__closed_bracket = "<", ">"
        
        # negative and positive infinity symbol,
        # e.g. -inf, +inf
        self.__infinity_symbol = "-inf", "+inf"
        
        # decimal separator, e.g. ".", ","
        self.__decimal_separator = "."
        
        # interval members separator
        self.__members_separator = ";"
        
        self.compile_reader()
        
        
    def compile_reader(self):

        left_bracket_open = re.escape(self.open_bracket[0])
        left_bracket_closed = re.escape(self.closed_bracket[0])
        
        right_bracket_open = re.escape(self.open_bracket[1])
        right_braket_closed = re.escape(self.closed_bracket[1])
        
        # e.g. (   <    |   \(    ) 
        #      (   {}   |   {}    )
        left_bracket_regex_string = "({}|{})".format(
            left_bracket_open,
            left_bracket_closed
        )
        
        # e.g. (   >   |   \)    ) 
        #      (   {}   |   {}    )
        right_bracket_regex_string = "({}|{})".format(
            right_bracket_open,
            right_braket_closed
        )
        
        # ((   \d+  (?:  \.   (?:\d)+  )?   )|-inf)
        # (   \d+  (?:  {}   (?:\d)+  )?   )
        left_number_regex_string = "(\-?\d+(?:{}(?:\d)+)?|{})".format(
            re.escape(self.decimal_separator),
            re.escape(self.infinity_symbol[0]),
        )
        
        
        # ((   \d+  (?:  \.   (?:\d)+  )?   )|+inf)
        # (   \d+  (?:  {}   (?:\d)+  )?   )
        right_number_regex_string = "(\-?\d+(?:{}(?:\d)+)?|{})".format(
            re.escape(self.decimal_separator),
            re.escape(self.infinity_symbol[1]),
        )
        
        members_separator_regex = "{}".format(
            re.escape(self.members_separator)
        )
        
        
        interval_regex_string = "{}{}{}{}{}".format(
            left_bracket_regex_string,
            left_number_regex_string,
            members_separator_regex,
            right_number_regex_string,
            right_bracket_regex_string
        )
        
        self.__interval_regex = re.compile(interval_regex_string)
        
        
    def read(self, interval_string):
        # returns array of results, take first member
        args = self.__interval_regex.findall(interval_string)[0]
        
        left_bracket, minval, maxval, right_bracket = args
        
        left_inclusive = True if left_bracket == self.closed_bracket[0] else False
        right_inclusive = True if right_bracket == self.closed_bracket[1] else False
        
        
        minval_final = float(minval) if minval != self.infinity_symbol[0] else np.NINF 
        maxval_final = float(maxval) if maxval != self.infinity_symbol[1] else np.PINF
        
        interval = Interval(
            minval_final,
            maxval_final,
            left_inclusive,
            right_inclusive
        )
        
        return interval
      
        
    # boilerplate getter/setter code    
    
    @property
    def open_bracket(self):
        return self.__open_bracket
    
    @open_bracket.setter
    def open_bracket(self, val):
        self.__open_bracket = val
        return self
    
    @property
    def closed_bracket(self):
        return self.__closed_bracket
    
    @closed_bracket.setter
    def closed_bracket(self, val):
        self.__closed_bracket = val
        return self
        
    @property
    def infinity_symbol(self):
        return self.__infinity_symbol
    
    @infinity_symbol.setter
    def infinity_symbol(self, val):
        self.__infinity_symbol = val
        return self
    
    @property
    def decimal_separator(self):
        return self.__decimal_separator
    
    @decimal_separator.setter
    def decimal_separator(self, val):
        self.__decimal_separator = val
        return self
    
    @property
    def members_separator(self):
        return self.__members_separator
    
    @members_separator.setter
    def members_separator(self, val):
        self.__members_separator = val
        return self
    
    
        
interval_reader = IntervalReader()

interval_reader.compile_reader()

interval_reader.read("<1.2;2.3>")