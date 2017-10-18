# -*- coding: utf-8 -*-

from agglomerate import Agglomerate
import visual as vs

class Star(Agglomerate):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, body, pos, radius, color=vs.color.white, material=None, texture=None, makeTrail=True, rings=False ):
        Agglomerate.__init__( self, body, pos, radius, color, material, texture, makeTrail, rings )

        # add local light source (set at pos of the star)
# the color must be replaced through a function, which determines the color of the star out of its effective temperatur (black body)
        vs.local_light( pos   = pos,      
                        color = color
                      )
