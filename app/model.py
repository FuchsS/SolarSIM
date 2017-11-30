# -*- coding: utf-8 -*-

from helpers.exp_object import eObject # a custom object that can be expanded with the dot notation to add properties

import visual as vs
import Image

from objects.star       import Star
from objects.planet     import Planet
from objects.moon       import Moon

import math

def init(  ):
    """
        Create and initialize all celestial objects of the solar system.

    """


    
    # ADD A BACKGROUND (Optional)
    """
        Add a background image as a sphere at the origin (0, 0, 0)
    """
    backgroundImage     = Image.open( './textures/milky way.jpg' )
    background          = vs.sphere( radius = 300 )
    background.material = vs.materials.texture( data    = backgroundImage,
                                                mapping = "spherical"
                                              )
    background.opacity  = 0.9


    
    # INITIALIZE ALL OBJECTS
    """
        Every object has the following properties:
        
        name             = name of the object
        mass             = mass in kilogramm [kg]
        radius           = radius in meter [m]
        tilt             = inclination of the rotational axis [°]
        precession       = orientation of the rotational axis # now just a sign, later in degree [°]
        rotationPeriod   = rotation period around the objects own axis in days [d]; positive value=clockwise || negative value=counterclockwise
        barycenter       = center of mass around which two or more bodies orbit [now: celestial object; should be coordinates which are automatically detected]
        a                = semi-major axis is one half of the major axis, and thus runs from the centre to the perimeter of the orbit [m]
        e                = eccentricity, measure of how much the orbit deviates from being circular (without unit)
        theta0           = optional: starting angle in radian [rad], default is 0
        orbitalDirection = optional: flight direction around the barycenter, default is -1; positive value=clockwise || negative value=counterclockwise
              
    """
    sun = Star(
        name              = "Sun",
        mass              = 1.98855 * 10**30,
        radius            = 6.957 * 10**8,
        tilt              = 0,
        precession        = 1, # +1/-1
        rotationPeriod    = 25.05,
        barycenter        = (0, 0, 0),
        a                 = 0,
        e                 = 0,
        theta0            = 0,
        orbitalDirection  = -1,
    )
#    mercury    = Planet( "Mercury"   , 3.3011  * 10**23, 2.4397 * 10**6,     58.646,     sun, 5.790905   * 10**10, 0.2056300 )
#    venus      = Planet( "Venus"     , 4.86750 * 10**24, 6.0518 * 10**6,   -243.025,     sun, 1.08208    * 10**11, 0.0067720 )
    earth = Planet(
        name              = "Earth",
        mass              = 5.97237 * 10**24,
        radius            = 6.371  * 10**6,
        tilt              = 23.44, # today: 23.44; min: 22.1; max: 24.5
        precession        = 1,
        rotationPeriod    = 0.99726968,
        barycenter        = sun,
        a                 = 1.49598023 * 10**11,
        e                 = 0.017 # today: 0.0167086; min: 0.000055; max: 0.0679
    )
#    mars       = Planet( "Mars"      , 6.41710 * 10**23, 3.3895 * 10**6,   1.025957,     sun, 2.279392   * 10**11, 0.0934000 )
#    jupiter    = Planet( "Jupiter"   , 1.89860 * 10**27, 6.9911 * 10**7, 0.41354167,     sun, 7.78299    * 10**11, 0.0484980 )
#    saturn     = Planet( "Saturn"    , 5.68360 * 10**26, 5.8232 * 10**7,   0.439583,     sun, 1.429      * 10**12, 0.0555500 )
#    uranus     = Planet( "Uranus"    , 8.68100 * 10**25, 2.5362 * 10**7,   -0.71833,     sun, 2.87504    * 10**12, 0.0463810 )
#    neptune    = Planet( "Neptune"   , 1.02430 * 10**26, 2.4622 * 10**7,     0.6713,     sun, 4.50445    * 10**12, 0.0094560 )
#    pluto      = Planet( "Pluto"     , 1.303   * 10**22, 1.187  * 10**6,   6.387230,     sun, 5.90638    * 10**12, 0.2488    )
#    moon       =   Moon( "Moon"      , 7.34200 * 10**22, 1.7371 * 10**6,  27.321661,   earth, 3.84399    * 10**8 , 0.0549000 )


    
    # CREATE 3D MODELS
    """
        Every object has a 3D model with the following properties:
        
        pos              = position of the model within the animation as vector(x, y, z)
        radius           = radius of the model
        color            = optional: color of the model, default is vs.color.white
        material         = optional: a material such as marble as texture for a model, default is None
        texture          = optional: alternatively an image can be loaded as texture, default is None
        showTrail        = optional: if True a curve will be drawn as trail, default is True
        rings            = optional: texture of rings around the model, default is False
              
    """
#    sun.createModel( pos       = (0, 0, 0),
#                     radius    = 1,
#                     color     = vs.color.white,
#                     material  = None,
#                     texture   = './textures/sun.jpg',
#                     makeTrail = False,
#                     rings     = False
#                   )
#    mercury.createModel   ( (  2, 0, 0),  0.3, texture='./textures/mercury.jpg')
#    venus.createModel     ( (  6, 0, 0),  0.4, texture='./textures/venus.jpg'  )
#    earth.createModel     ( (  9, 0, 0),  0.5, material=vs.materials.BlueMarble)
#    mars.createModel      ( ( 12, 0, 0), 0.45, texture='./textures/mars.jpg'   )
#    jupiter.createModel   ( ( 20, 0, 0),  0.8, texture='./textures/jupiter.jpg', rings='./textures/jupiters rings.png')
#    saturn.createModel    ( ( 28, 0, 0),  0.7, texture='./textures/saturn.jpg' , rings='./textures/saturns rings.png' )
#    uranus.createModel    ( ( 36, 0, 0),  0.6, texture='./textures/uranus.jpg' , rings='./textures/uranus rings.png'  )
#    neptune.createModel   ( ( 45, 0, 0),  0.6, texture='./textures/neptune.jpg', rings='./textures/neptunes rings.png')
#    pluto.createModel     ( ( 65, 0, 0),  0.2, texture='./textures/pluto.png'  )
#    moon.createModel      ( (9.9, 0, 0),  0.2, texture='./textures/moon.jpg', makeTrail=False )
#    moon.model.velocityVector = vs.vector( 0.9,   0,   0)
    
    # realisitic distance ratio
    sun.createModel    ( (0, 0, 0), 1, color=vs.color.white, texture='./textures/sun.jpg', makeTrail=False)
#    mercury.createModel( (3.87, 0, 0),  0.3, texture='./textures/mercury.jpg')
#    venus.createModel  ( (7.23, 0, 0),  0.4, texture='./textures/venus.jpg'  )
    earth.createModel  ( (10, 0, 0),  0.5, texture='./textures/earth.jpg') # Attention: material='Blue Marble' causes a bug, when stopping and starting the simulation again
#    mars.createModel   ( (15.24, 0, 0), 0.45, texture='./textures/mars.jpg'   )
#    jupiter.createModel( (52.03, 0, 0),  0.8, texture='./textures/jupiter.jpg', rings='./textures/jupiters rings.png')
#    saturn.createModel ( (95.52, 0, 0),  0.7, texture='./textures/saturn.jpg' , rings='./textures/saturns rings.png' )
#    uranus.createModel ( (192.18, 0, 0),  0.6, texture='./textures/uranus.jpg' , rings='./textures/uranus rings.png'  )
#    neptune.createModel( (301.10, 0, 0),  0.6, texture='./textures/neptune.jpg', rings='./textures/neptunes rings.png')
#    pluto.createModel  ( (394.82, 0, 0),  0.2, texture='./textures/pluto.png'  )
#    moon.createModel   ( (10.03, 0, 0),  0.2, texture='./textures/moon.jpg', makeTrail=False )
#    moon.model.velocityVector = vs.vector( 0.9,   0,   0)

    # ADDING OBJECTS TO THE MODEL
    model              = eObject()
    model.stars        = [ sun ]
#    model.stars        = [  ]
    model.planets      = [ earth ]
    model.moons        = [  ]
#    model.planets      = [ mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, pluto ]
#    model.moons        = [ moon ]
    model.solarSystem  = model.stars[:] + model.planets[:] + model.moons[:]
    
    # COMPARE OBJECTS   - creates compareable objects with all characteristics of the originals, only the eccentricity will be set to zero
    comparisonList = [ earth ]
    comparisonList = model.planets
    comparisons = [  ]
#    for entry in comparisonList:
#        newObject = Planet( entry.name, entry.mass, entry.radius, entry.tilt, entry.precession, entry.rotationPeriod, entry.barycenter, entry.a, entry.e, entry.theta0, entry.orbitalDirection )
#        newObject.createModel( entry.model.initialPos, entry.model.radius,  material=vs.materials.BlueMarble, ) #color=vs.color.red )
#        newObject.model.visible = False # hide the object, so that only its trail is visible
#        newObject.model.axisFrame.visible = False # hide the object, so that only its trail is visible
#        comparisons.append(newObject)
    model.comparisons = comparisons
#    model.solarSystem += model.comparisons
    
    # DISPLAY INFOS OF THE FOLLOWING OBJECTS
    model.observations = [ earth ]

    return model
