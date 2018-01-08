# -*- coding: utf-8 -*-

import visual as vs # for 3D panel
import Image
from particle import Particle

class Agglomerate(Particle):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, body, pos, radius, color, material, texture, showTrail, rings ):
        Particle.__init__( self, body, pos, radius, color, material, texture, showTrail )

        self.rings = rings
        
        if rings:
            self.rings = vs.ellipsoid( pos=self.pos, size=( self.radius * 4, 0.01, self.radius * 4 ), opacity=0.95 )
            width    = 512 # must be power of 2
            height   = 512 # must be power of 2
            image    = Image.open(rings)
            image    = image.resize( (width, height), Image.ANTIALIAS )
            material = vs.materials.texture( data=image, mapping="cubic")

            self.rings.material = material
