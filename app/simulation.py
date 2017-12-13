# -*- coding: utf-8 -*-

from __future__ import division
import math
import wx
from gui.animation.scene import Scene       # for the animation
from helpers.conversion.time import *
import model as model
import visual as vs
from objects.planet     import Planet
from helpers.namer import fn_namer

# constants
DAY  = 86400                           # mean solar day [s]
YEAR = 365.25                          # a solar year is a circulation of the earth on its orbit around the sun or the time required for it [days]
S    = 1367                            # so called solar constant at a distance of 1 AU [W/m²]
AU   = 1.49598023 * 10**11             # astronomical unit: length of the semi-major axis [m]


class Simulation:

    def __init__(self, panel, stepSize, speed, eccentricity, tilt, precession):
        self.panel      = panel
        
        # Creates the animation
        self.animation = Scene(title="SolarSIM", x=400, y=0, width=800, height=800, center=(10, 0, 0) ).scene
        self.system = model.init()

        # Set settings
        self.stepSize     = stepSize
        self.speed        = speed
        self.eccentricity = eccentricity
        self.tilt         = tilt
        self.precession   = precession

    # ----------------------------------------------------------------------------
    # RUN SIMULATION                     
    # ----------------------------------------------------------------------------
    @fn_namer
    def runSimulation(self):
        print( "Simulation settings:")
        print( "• stepSize: {} seconds".format( self.stepSize ) )
        print( "• speed: {}".format( "{}x".format( self.speed ) ) )
        print( "Orbital settings:")
        print( "• eccentricity: {:f}".format( self.eccentricity ).rstrip('0') )
        print( "• tilt: {:.2f}°".format( self.tilt ) )
        print( "• precession: {}".format( self.precession ) )
        
        self.setOrbitalParameters(old=self.system.observation, eccentricity=self.eccentricity, tilt=self.tilt, precession=self.precession )
        
        statusBar = self.panel.statusBar
        
#        self.panel.data1 = []
#        self.panel.data2 = []
        
        t  = self.stepSize
        timeStep = 0
        system = self.system

        self.isStopped = False
        self.running   = True
        while self.running:
            dt = self.stepSize
            
            # Lasting trail
            for body in system.solarSystem:
                if body.model.makeTrail:
                    body.model.setMaxTrail( 0.9 * self.stepSize )
            
            vs.rate(self.speed)
            
            # PLANETS
#            for planet in system.planets + system.comparisons:
            for planet in system.planets:
                
                # Checks if the simulation should be stopped in between
                if(not self.running):
                    break
                
                self.currentObject = planet
                
                # DISPLAY INFOS
                if planet == system.observation:

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
            self.panel.data1.append(self.panel.datagen.next())
            self.panel.data2.append(-self.panel.data1[-1])
#            self.panel.draw() # live drawing (really slow)
            t += dt
            timeStep += 1
        
        self.isStopped = True
        self.panel.draw() # draw the charts at the end of the simulation
        # Cleaning up
        wx.CallAfter(self.cleanupSimulation)


    @fn_namer
    def stopSimulation(self):
        self.running = False


    @fn_namer
    def cleanupSimulation(self):
        # Deletes the animation
        self.animation.delete()
        
    
    @fn_namer
    def setOrbitalParameters(self, old, tilt=False, precession=False, eccentricity=False):

# TO DO: Create a function DeepCopy
        # Create a new object
        if not tilt:
            tilt         = old.tilt
        if not precession:
            precession   = old.precession
        if not eccentricity:
            eccentricity = old.e
        new = Planet(
            old.name,
            old.mass,
            old.radius,
            tilt, # new value
            precession, # new value
            old.rotationPeriod,
            old.barycenter,
            old.a,
            eccentricity, # new value
            old.theta0,
            old.orbitalDirection
        )
        new.createModel(
            old.model.pos,
            old.model.radius, 
            material=old.model.material
        )
			
        # Delete all list entries of the old object and create entries for the new object
        for aList in [self.system.stars, self.system.planets, self.system.moons, self.system.solarSystem, self.system.comparisons]:
            if old in aList:
                aList.remove(old)
                aList.append(new)
        
        # Delete the old object itself
        old.model.visible = False
        old.model.axisFrame.visible = False
        del old
        
    
    @fn_namer
    def ChangeSimulationStepsize(self, value):
        self.stepSize = value
    
    
    @fn_namer
    def ChangeSimulationSpeed(self, value):
        self.speed    = value
