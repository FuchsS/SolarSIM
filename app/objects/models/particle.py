# -*- coding: utf-8 -*-

from __future__ import division
import math

import visual as vs # for 3D panel
import Image

class Particle( vs.sphere ):
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__( self, body, pos, radius, color, material, texture, makeTrail ):
        """
            Every object has a 3D model with the following properties:
            
            pos              = position of the model within the animation as vector(x, y, z)
            radius           = radius of the model
            color            = optional: color of the model, default is vs.color.white
            material         = optional: a material such as marble as texture for a model, default is None
            texture          = optional: alternatively an image can be loaded as texture, default is None
            showTrail        = optional: if True a curve will be drawn as trail, default is True
              
        """        
        vs.sphere.__init__( self, pos=pos, radius=radius, color=color, make_trail=False )
        self.body       = body
        self.makeTrail  = makeTrail
        self.initialPos = pos
        
        # DETERMINE POSITION AND ORBITAL SETTINGS
        self.a = self.x
        self.b = self.a - (body.e * self.a)
        direction = body.orbitalDirection
        if   math.cos(body.theta0) == 0:
            self.orbitalDirection = vs.vector( direction, 1, 1)
        elif math.sin(body.theta0) == 0:
            self.orbitalDirection = vs.vector( 1, 1, direction)
        else:
            self.b *= -1 # because z.axis is in the "wrong" direction (in vpython)
            self.orbitalDirection = vs.vector( -direction, 1, 1)
        self.x = self.a * ( math.cos(body.alpha) + body.e) # x-coordinate from the barycenter (x + e    with e = a · ε)
        self.z = self.b * math.sin(body.alpha) # z is actually y (in vpython)

        # ADD TEXTURE IMAGE
        if texture:
            width    = 1024 # must be power of 2
            height   = 512  # must be power of 2
            image    = Image.open( texture )
            image    = image.resize( (width, height), Image.ANTIALIAS )
            material = vs.materials.texture( data=image, mapping="spherical" )
        self.material = material
        
        # SET TRAIL
        self.make_trail = self.makeTrail
        self.trail_type = 'curve'       # the default type is "curve", but can be "points"
        self.interval   = 10            # a point is added to the trail every # move of the object

        # DISPLAY NAME
        print(body.name)



    # METHODES
    def setMaxTrail( self, stepSize ):
        period            = self.body.orbitalPeriod
        stepsForOnePeriod = (period/stepSize)
        trailInterval     = self.interval
        # The trail of each particle should only last for one period
        self.retain       = int(stepsForOnePeriod/trailInterval)
