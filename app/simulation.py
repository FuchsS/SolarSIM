# -*- coding: utf-8 -*-

from __future__ import division
import math

from helpers.conversion.time import *
import model as model
import visual as vs
from objects.planet     import Planet

# constants
DAY  = 86400                           # mean solar day [s]
YEAR = 365.25                          # a solar year is a circulation of the earth on its orbit around the sun or the time required for it [days]
S    = 1367                            # so called solar constant at a distance of 1 AU [W/m²]
AU   = 1.49598023 * 10**11             # astronomical unit: length of the semi-major axis [m]


settings = {
    'duration' : 3/3*YEAR * DAY,
#    'duration' : 88 * DAY,
#    'stepSize' : timeHoursSeconds(10000,0,0,0),
#    'stepSize' : 21600, # 1461 Schritte auf 1 Jahr (geht genau auf!)
#    'stepSize' : DAY,
    'stepSize' : 3600,
#    'stepSize' : 1800,
#    'stepSize' : 60,
#    'stepSize' : 1,
    'speed'    : 1,
#    'speed'    : 10000000000000000000000000000,
#    'speed'    : 1
    }



class Simulation():
    def __init__(self, *args, **kwargs):
        


        # getSettings
        self.duration = settings['duration']
        self.stepSize = settings['stepSize']
        self.speed    = settings['speed']
        self.timeStep = 0

    # ----------------------------------------------------------------------------
    # RUN SIMULATION                     
    # ---------------------------------------------------------------------------- 
    def run(self, animation, panel):
        
        self.system = model.init(  )

        animation = animation.scene.infoLabel
        statusBar = panel.statusBar
        
        
        t  = self.stepSize
#        while t <= self.duration:
        while True:
            dt = self.stepSize
            system = self.system
            
            # Lasting trail
            for body in system.solarSystem:
                if body.model.makeTrail:
                    body.model.setMaxTrail( 0.9 * self.stepSize )
            
            vs.rate(self.speed)
            
            # PLANETS
#            for planet in system.planets + system.comparisons:
            for planet in system.planets:
                self.currentObject = planet
                
                # DISPLAY INFOS
                if planet in system.observations:

                    r = planet.orbitalDistance/AU
                    I = S/(4 * r**2)
                    J = S/(4 * math.sqrt(1 - planet.e**2))
                    statusBar.SetStatusText(
                        ( "Time: {:.2f} years,"            + "    "
                          "Distance: {:.2f} AU,"           + "    "
                          "Orbital velocity: {:.2f} km/s," + "    "
                          "Rotational velocity: {:.3f} km/s"
                        ).format(
                            t/DAY/YEAR,
                            r,
                            planet.orbitalVelocity/1000,
                            planet.rotationalVelocity/1000
                        )
                    )
                    # DEBUG
#                    debug = "%s \t %.14f \t %.14f" % ( t, planet.orbitalAngularVelocity, planet.get_deltaOrbitalAngularPosition( t, dt ) )
                
                # ORBIT AROUND THE BARYCENTER
                planet.orbit( t, dt )
                
                # DEBUG
                planet.distance += dt * planet.orbitalVelocity
                planet.meanVelocity += planet.orbitalVelocity
                if planet.printed == False and round(math.degrees(planet.alpha), 1) >= math.degrees(planet.theta0) + 360:
#                if True:
                    planet.printed = True
                    eccentricity = planet.e == 0 and str(0) or str("%.7f" % planet.e)
                    print( "\nPeriod of %s (with eccentricity = %s):"  % (planet.name, eccentricity) )
                    print( "· according to Keplerian laws: %.6f" % ( planet.orbitalPeriod/DAY ) )
                    print( "· in the Simulation: %.6f" % ( t/DAY ) )
                    print( "· traveled distance: %.2f km" % (planet.distance/1000) )
                    print( "· mean velocity: %.2f km/s" % (planet.meanVelocity/( t/dt )/1000) )
                                    
                    
                
#                if planet in system.observations:
#                    debug += "\t %.14f \t %.14f \t %s \t %s" % ( planet.alpha, planet.r, planet.model.pos.x, planet.model.pos.z )
#                    print( debug.replace( '.', ',' ) )

            for planet in system.comparisons:
                # ORBIT AROUND THE BARYCENTER
                planet.orbit( t, dt )

            # MOONS
            for moon in system.moons:
#                moon.orbit( t, dt )
                moon.model.velocityVector = vs.rotate( vector = moon.model.velocityVector,
                                                       angle  = moon.get_deltaOrbitalAngularPosition( t, dt ),
                                                       axis   = (0, -moon.orbitalDirection, 0)
                                                     )
                moon.model.pos = moon.barycenter.model.pos + moon.model.velocityVector

            # General transformation for all objects
            for body in system.solarSystem:
                # Simulate rotation around the objects own axis
                body.model.rotate( angle  = body.get_deltaRotationalAngularPosition( t, dt ),               # angle in radians [rad]
                                   axis   = body.model.rotationalAxis.axis # x, y, z
                                 )
                # Simulate movement and rotation of the object rings
                if body.model.rings:
                    body.model.rings.pos = body.model.pos
                    body.model.rings.rotate( angle  = body.get_deltaRotationalAngularPosition( t, dt ),     # angle in radians [rad]
                                             axis = body.model.rotationalAxis.axis # x, y, z
                                           )
                    
            for body in system.comparisons:
                # Simulate rotation around the objects own axis
                body.model.rotate( angle  = body.get_deltaRotationalAngularPosition( t, dt ),               # angle in radians [rad]
                                   axis   = body.model.rotationalAxis.axis # x, y, z
                                 )
                # Simulate movement and rotation of the object rings
                if body.model.rings:
                    body.model.rings.pos = body.model.pos
                    body.model.rings.rotate( angle  = body.get_deltaRotationalAngularPosition( t, dt ),     # angle in radians [rad]
                                             axis = body.model.rotationalAxis.axis # x, y, z
                                           )
            
            
            # PROGRESS IN TIME
            t += dt
            self.timeStep += 1

#    def ChangeEccentricity(self, value):
#        self.currentObject.e = value
        
    def ChangeOrbitalParameters(self, tilt=False, precession=False, eccentricity=False):
        this = self.currentObject
        
        # Delete the old object (incl. all list entries)
        for entry in self.system.comparisons:
            if this.name == entry.name:
                if tilt == False:
                    tilt = entry.tilt
                if precession == False:
                    precession = entry.precession
                if eccentricity == False:
                    eccentricity = entry.e
                entry.model.visible = False
                entry.model.axisFrame.visible = False
                self.system.comparisons.remove(entry)
                del entry
        for entry in self.system.observations:
            if this.name == entry.name:
                self.system.observations.remove(entry)
# TO DO: Create a function DeepCopy
        # Create the new object
        if tilt == False:
            tilt = this.tilt
        if precession == False:
            precession = this.precession
        if eccentricity == False:
            eccentricity = this.e
        newObject = Planet( this.name, this.mass, this.radius, tilt, precession, this.rotationPeriod, this.barycenter, this.a, eccentricity, this.theta0, this.orbitalDirection )
        newObject.createModel( this.model.pos, this.model.radius,  material=this.model.material )
#        newObject.model.a = this.model.a
#        newObject.model.b = this.model.b
#        newObject.model.orbitalDirection = this.model.orbitalDirection
        newObject
        
        self.system.comparisons.append(newObject)
        self.system.observations.append(newObject)
        
    

    def ChangeSimulationStepsize(self, value):
        self.stepSize = value
    
    def ChangeSimulationSpeed(self, value):
        self.speed    = value
