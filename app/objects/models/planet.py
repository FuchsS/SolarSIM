# -*- coding: utf-8 -*-

from agglomerate import Agglomerate
import visual as vs

class Planet(Agglomerate):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, body, pos, radius, color=vs.color.white, material=None, texture=None, makeTrail=True, rings=False ):
        Agglomerate.__init__( self, body, pos, radius, color, material, texture, makeTrail, rings )
