# -*- coding: utf-8 -*-

"""
    An object class that can be extended by the dot notation.

    Code example:

        coordinates = eObject()
        coordinates.x = 0
        coordinates.y = 0
        ...
    
"""
class eObject(object):
    
    def __init__(self):
        object.__init__(self)
        pass
