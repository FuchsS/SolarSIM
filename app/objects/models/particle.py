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
        alpha = body.alpha
        tilt = math.radians(body.tilt)
        precession = body.precession
        if type(pos) is int: # only for setOrbitalParameters (in Simulation)
            pos=vs.vector( (pos, 0, 0) )
        vs.sphere.__init__( self, pos=pos, radius=radius, axis=vs.vector( math.cos(tilt), precession * math.sin(tilt), 0), color=color, make_trail=False )
        self.body       = body
        self.makeTrail  = makeTrail
        self.initialPos = pos
        self.a = self.x
        
        # ADD A ROTATIONAL AXIS
        self.axisFrame = vs.frame( pos=pos )
        x = precession * math.sin(tilt)
        y = math.cos(tilt)
        z = 0
        self.rotationalAxis = vs.arrow( 
                frame       = self.axisFrame, 
                pos         = vs.vector(  x, -y * 2 * radius, z),
                axis        = vs.vector( -x,  y, z),
                length      = 4. * radius, 
                shaftwidth  = 0.01,
                headwidth   = 0.01,
                headlength  = 0.01,
                color       = color 
        )
        
        # DETERMINE POSITION AND ORBITAL SETTINGS
        e = body.e
        a = self.a
        r = a + ( -math.sin(alpha) * a * e )
        x = -math.sin(alpha) * r
        z = -math.cos(alpha) * r
        self.pos           = (x, 0, z) # move planet
        self.axisFrame.pos = (x, 0, z) # move rotational axis
        
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
        print("--")



    # METHODES   
    def setMaxTrail( self, stepSize ):
        period            = self.body.orbitalPeriod
        stepsForOnePeriod = (period/stepSize)
        trailInterval     = self.interval
        # The trail of each particle should only last for one period
        self.retain       = int(stepsForOnePeriod/trailInterval)
