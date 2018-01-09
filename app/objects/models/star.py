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

# the color must be replaced through a function, which determines the color of the star out of its effective temperatur (black body)
        # In order to make the sun shine, we place light sources around it.
        color = vs.color.gray(0.6)
        distance = radius+0.5
        pos = (-distance, +distance)
        for x in pos:
            for y in pos:
                for z in pos:
                    # debug
#                    print("x={:2}, y={:2}, z={:2}".format(x, y, z))
                    vs.local_light( pos   = (x, y, z),     
                                    color = color
                                  )