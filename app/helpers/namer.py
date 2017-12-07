# -*- coding: utf-8 -*-
"""
    Namer
    A simple way to record which function is called in which order is to 
    define a decorator which prints the called function. Then, you have 
    to add this decorator before the function, like
    
        @fn_namer
        def myfunction(...):
            ...
    
    Author: Stefan Fuchs

"""

from functools import wraps

def fn_namer(function):
    @wraps(function)
    def function_namer(*args, **kwargs):
        print( "--" )
        print( "called: {}".format(function.func_name) )
        result = function(*args, **kwargs)
        return result
    return function_namer