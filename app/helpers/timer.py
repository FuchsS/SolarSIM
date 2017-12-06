# -*- coding: utf-8 -*-
"""
    Timer
    A simple way to time a function is to define a decorator that measures the 
    elapsed time in running the function, and prints the result. Then, you have 
    to add this decorator before the function you want to measure, like
    
        @fn_timer
        def myfunction(...):
            ...
    
    Source:
        http://www.marinamele.com/7-tips-to-time-python-scripts-and-control-memory-and-cpu-usage

"""
import time
from functools import wraps

def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print ("Total time running %s: %s seconds" %
               (function.func_name, str(t1-t0))
               )
        return result
    return function_timer