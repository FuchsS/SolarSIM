# -*- coding: utf-8 -*-

#############################
# Module:   MenuBar
# Author:   S.Fuchs
# Date:     2016/07/05
# Version:  Entwurf 0.1
#
# Beschreibung: Menubar
#
###############################
# Log:
# 2016/07/05    SF - Datei erzeugt
################################
""" Description:
    
    Contains the menubar
    
"""

import visual as vs # for 3D panel
import Image

class Scene:
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__(self, title, x, y, width, height, center):
        """
        Initialise the scene.
        
        __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True, processes=[ ], taskQueue=[ ], doneQueue=[ ], tasks=[ ])
            
            Parameters:

                title         - Text in the window's title bar.                
                x, y          - Position of the window on the screen (pixels from upper left).
                width, height - Width and height of the display area in pixels.
    !BUG!       fullscreen    - Full screen option. Makes the display take up the entire screen.
                visible       - Make sure the display is visible.
                ...
                lights        - List of distant light objects created for this display.
                ambient       - Color of nondirectional ("ambient") lighting.
                ...
                center        - Location at which the camera continually looks, even as the user rotates the position of the camera.
                forward       - Vector pointing in the same direction as the camera looks.
                range         - The extent of the region of interest away from center along each axis.
                ...
    
        """

        # Create a 3D animation scene
        self.scene = vs.display(
            title   = title,
            x       = x,
            y       = y,
            width   = width,
            height  = height,
#            fullscreen = True, # BUG: In full screen mode, the simulation can not be stopped without crashing.
            lights  = [],
#            ambient = 0, # color of the ambient light (0=no ambient light, with realistic shadows)
#            ambient = vs.color.gray(0.6), # compromise
#            ambient = vs.color.white, # color of the ambient light (= bright light, hardly any shadows)
            center  = center,
#            forward = (-1,0,0),
            range   = 12,
        )
        
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
        
        # ADD AXES
#        self.showAxes( None, vs.color.white, 3, (0,0,0))# (-11, 6, 0))
            


        # Set some program flags
        self.isPaused = False
        
        # Event handler
        self.scene.bind( 'mousedown', self.OnMouseDown) # mouse pressed event
        self.scene.bind( 'keydown', self.OnKeyPress) # key pressed event
        
    
    # Make axes visible (of world or frame).
    def showAxes( self, frame, color, length, pos ): # Use frame=None for world.
        directions = [ vs.vector(length, 0, 0), vs.vector(0, length, 0), vs.vector(0, 0, length) ]
        texts = ["x","y","z"]
        pos = vs.vector(pos)
        for i in range(3): # each direction
           vs.curve( frame=frame, color=color, pos=[pos, pos+directions[i]])
           vs.label( frame=frame, color=color, pos=pos+directions[i], text=texts[i], opacity=0, box=False )

    
    # EVENTS        
    def OnMouseDown(self, event):
        scene = self.scene
        scene.center = scene.mouse.pos # focus camera on new position
        
    # Handler of a key pressed event
    def OnKeyPress(self, event):
        keycode = event.key
#        print keycode
        if keycode == ' ': # spacebar pressed => Pause/Resume
            self.OnPause('keydown spacebar')
    
    # Spacebar pressed => Pause/Resume
    def OnPause(self, event):
        self.isPaused = not self.isPaused
        while self.isPaused:
            self.scene.waitfor('keydown')
