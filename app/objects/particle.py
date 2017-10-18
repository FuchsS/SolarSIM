# -*- coding: utf-8 -*-

from __future__ import division
import math

from helpers.conversion.time import *

from models.particle import Particle



# constants
G      = 6.67408    * 10**-11   # gravitational constant [ m³ / (kg ⋅ s²) ]
AU     = 1.49598023 * 10**11    # astronomical unit: length of the semi-major axis [AU]
Msun   = 1.98855    * 10**30    # solar mass as standard unit [solar masses]
Rearth = 6.371      * 10**6     # Earth's mean radius [m]

DAY  = 86400                    # mean solar day [s]
YEAR = 365.25                   # a solar year is a circulation of the earth on its orbit around the sun or the time required for it [days]



class Particle(object):
    """
        Every object has the following properties:
        
        name             = name of the object
        mass             = mass in kilogramm [kg]
        radius           = radius in meter [m]
        rotationPeriod   = rotation period around the objects own axis in days [d]; positive value=clockwise || negative value=counterclockwise
        barycenter       = center of mass around which two or more bodies orbit [now: celestial object; should be coordinates which are automatically detected]
        a                = semi-major axis is one half of the major axis, and thus runs from the centre to the perimeter of the orbit [m]
        e                = eccentricity, measure of how much the orbit deviates from being circular (without unit)
        theta0           = optional: starting angle in radian [rad], default is the aphelion at 0 · π (0 °)
        orbitalDirection = optional: flight direction around the barycenter, default is -1; positive value=clockwise || negative value=counterclockwise
        
        alpha            = current orbital angular position from the aphelion
        r                = current distance from the barycenter
              
    """
    
    # CONSTRUCTOR
    def __init__(self, name, mass, radius, rotationPeriod, barycenter, a, e, theta0=0*math.pi, orbitalDirection=-1 ):
        self.name             = name
        self.mass             = mass
        self.radius           = radius
        self.rotationPeriod   = rotationPeriod
        self.barycenter       = barycenter
        self.a                = a
        self.e                = e
        self.theta0           = theta0
        self.orbitalDirection = orbitalDirection
        
        self.alpha            = theta0
        
        # Debug
        self.printed          = False
        self.distance         = 0
        self.meanVelocity     = 0


    
    @property
    def r( self ):
        return self.orbitalDistance
    
    
    @property
    def orbitalDistance( self ):
        r = self.a * ( 1 + self.e * math.cos(self.alpha) )
        return r
    
    
    @property
    def orbitalAngularVelocity( self ):
        w = ( G * self.barycenter.mass / self.r**3 )**0.5
        return w
    
    
    @property
    def orbitalVelocity( self ):                                          # returns [m/s]
        """
            Die Orbitalgeschwindigkeit des Planeten bei seinem derzeitigem Abstand vom Massezentrum.
        """
        velocity = self.orbitalAngularVelocity * self.r        # current orbital velocity [m/s]
        return velocity


    @property
    def orbitalPeriod( self ):
        p = ( (4 * math.pi**2 * self.a**3) / (G * (self.barycenter.mass + self.mass)) )**0.5
        return p

        
    def get_orbitalAngularPosition( self, t ):
        angle = self.theta0 + self.orbitalAngularVelocity * t
        return angle


    def get_deltaOrbitalAngularPosition( self, t, dt ):
        dangle = self.get_orbitalAngularPosition( t ) - self.get_orbitalAngularPosition( t-dt )
        return dangle
    
    
    def orbit( self, t, dt ):
        self.alpha += self.get_deltaOrbitalAngularPosition( t, dt )
#        if ( self.alpha > 2 * math.pi ):
#            self.alpha -= 2 * math.pi
        x  = self.model.a * ( math.cos(self.alpha) + self.e ) # x-coordinate from the barycenter (x + e    with e = a · ε)
        z  = self.model.b * math.sin(self.alpha)
        x *= self.model.orbitalDirection.x
        z *= self.model.orbitalDirection.z
        self.model.pos = (x, 0, z)



    @property
    def rotationalAngularVelocity( self ):                                # returns [rad/s]
        """
            Die Rotation pro Sekunde beschrieben durch die Winkelgeschwindigkeit in Radian [rad]. 

            Die vollständige Drehung eines beliebigen Planeten um seine Achse entspricht einem Vollkreis (360°).
            Ein Vollkreis hat die Bogenlänge U=2·π·r, weshalb der Vollwinkel 2·π beträgt. Dieser wird durch die
            benötigte Zeit in Sekunden geteilt. Das Ergebnis entspricht der Winkelgeschwindigkeit pro Sekunde [rad/s].
        """
        circumference     = (2 * math.pi)                               # the circumference of a planet can be approximated as a circle
        rotationInSeconds = self.rotationPeriod * DAY                           # seconds that are necessary for a whole rotation
        velocity          = circumference/rotationInSeconds             # angular velocity per second [rad/s]
        return velocity


    def get_rotationalAngularPosition(self, t):                             # returns [rad]
        """
            Der Winkel, um den sich ein Planet zu einem bestimmten Zeitpunkt gedreht hat; Winkel in Radian [rad]. 

            Der Winkel ergibt sich durch die Winkelgeschwindigkeit, die mit der verstrichenen Zeit multipliziert
            und auf den Startwinkel addiert wird.
        """
        angle = self.theta0 + self.rotationalAngularVelocity * t      # angular position [rad]
        return angle



    def get_deltaRotationalAngularPosition(self, t, dt):                        # returns [rad]
        """
            Die Änderung des Winkels zwischen zwei Zeitschritten; Winkel in Radian [rad]. 

            Die Änderung entspricht der Differenz der Winkelpositionen vom letzten und aktuellen Zeitpunkt.
        """
        dangle = self.get_rotationalAngularPosition( t ) - self.get_rotationalAngularPosition( t-dt )     # delta angular position [rad]
        return dangle


    @property
    def rotationalVelocity( self ):                                          # returns [m/s]
        """
            Die Rotationsgeschwindigkeit des Planeten.

            Die Geschwindigkeit ergibt sich aus dem Umfang des Planeten geteilt durch die benötigte Zeit
            für eine vollständige Umdrehung.
        """
        circumference     = (2 * math.pi * self.radius)                    # circumference of the planet [m]
        rotationInSeconds = self.rotationPeriod * DAY                        # seconds that are necessary for a whole rotation
        velocity          = circumference / rotationInSeconds              # rotational velocity [m/s]
        return velocity


    @property
    def gravitationalForce( self ):
        f = G * self.mass * self.barycenter.mass / self.r**2
        return f


    # MODELS
    def createModel( self, *args, **kwargs ):
        self.model = modelType.Particle( self, *args, **kwargs )
    
#    def createCompareableModel( self, *args, **kwargs ):
#        self.model = modelType.Particle( self, *args, **kwargs )
