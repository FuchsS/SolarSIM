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
from constants import *

class Simulation:

    def __init__(self, panel, stepSize, speed, eccentricity, tilt, precession):
        self.panel      = panel
        
        # Creates the animation
        self.animation = Scene(title="SolarSIM", x=400, y=0, width=800, height=800, center=(0, 0, 0) ).scene
        self.system = model.init(eccentricity, tilt, precession)

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
        
        t        = self.stepSize
        timeStep = 0
        system   = self.system

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
                    
                # CALCULATE INSOLATION
                if ( t%DAY == 0 or dt == DAY): # only once a day
                    # If one year has passed
#                    oneYearPassed = planet.alpha > (planet.theta0 + 2*math.pi)
#                    print( oneYearPassed )
                    day   = round( t/DAY)
                    tilt  = planet.tilt
                    alpha = planet.alpha
                    delta = math.asin( -math.sin(tilt) * math.sin(alpha) )
                    r = planet.r/AU
                    a = planet.a/AU
                    # DEBUG
#                    print( "{} day".format(int(day)) )
#                    print( "· sun distance:        {:.2f} AU".format(r) )
#                    print( "· right ascension:     {:3.2f}°".format(math.degrees(alpha)) )
#                    print( "· declination:         {:3.2f}°".format(math.degrees(delta)) )
                    data = [  ]
                    for lat in range(-90, 91, 30): # for every latitude
                        lat = math.radians(lat)
                        h = math.acos( max( -1, min( +1, -math.tan(lat) * math.tan(delta) ) ) ) # hourAngleAtSunSet
                        I = (S * a**2)/(math.pi * r**2) * (h * math.sin(lat) * math.sin(delta) + math.sin(h) * math.cos(lat) * math.cos(delta))
                        data.append( (day, round( math.degrees(lat)), I) )
                        # DEBUG
#                        print( " {} deg".format( round( math.degrees( lat))))
#                        print( "· hour angle:      {:3.2f}°".format( math.degrees( h)) )
#                        print( "· solar radiation: {:.2f} W/m²".format( I) )
                    planet.data.append(data)
                
                
                    # If this is the planet which is beeing observed
                    if planet == system.observation:
                        # DEBUG
                        for entry in planet.data[-1]:
                            print( "{:.2f} {:.2f}".format(entry[1], entry[2]) )
                            print("--")
                        # Append data to chart data
                        self.panel.data2.append(planet.data[-1])
                        # Display infos in status bar
                        self.updateStatusBar(t, planet)
                                    

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
                # ORBIT AROUND THE BARYCENTER
                body.orbit( t, dt )
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
#            self.panel.data1.append(self.panel.datagen.next())
#            self.panel.data2.append(-self.panel.data1[-1])
#            self.panel.draw() # live drawing (really slow)
            t += dt
            timeStep += 1
        
        self.isStopped = True
#        self.panel.draw() # draw the charts at the end of the simulation
        # Cleaning up
        wx.CallAfter(self.cleanupSimulation)

    

#    @fn_namer
    def updateStatusBar(self, t, planet): # Display infos in the status bar
        self.panel.statusBar.SetStatusText(
            ( "Time: {:.2f} years,"            + "    "
              "Distance: {:.2f} AU,"           + "    "
              "Orbital velocity: {:.2f} km/s," + "    "
              "Rotational velocity: {:.3f} km/s"
            ).format(
                t/DAY/YEAR,
                planet.r/AU,
                planet.orbitalVelocity/1000,
                planet.rotationalVelocity/1000
            )
        )
            

    @fn_namer
    def stopSimulation(self):
        self.running = False


    @fn_namer
    def cleanupSimulation(self):
        # Deletes the animation
        self.animation.delete()
        
    
    @fn_namer
    def ChangeSimulationStepsize(self, value):
        self.stepSize = value
    
    
    @fn_namer
    def ChangeSimulationSpeed(self, value):
        self.speed    = value
