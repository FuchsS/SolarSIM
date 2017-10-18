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

class Scene:
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__(self):

        # 3D scene
        scene = vs.display( title   = "SolarSIM",                                         # title of the window
                            x       = 0,                                                  # x-position of the window on the screen (pixels from upper left)
                            y       = 0,                                                  # y-position of the window on the screen (pixels from upper left)
                            lights  = [],                                                 # deactivates distant default light sources
#                            ambient = 0,                                                 # color of the ambient light (0=no ambient ligt, with realistic shadows)
                            ambient = vs.color.gray(0.6),                                 # compromise
#                            ambient = vs.color.white,                                     # color of the ambient light (= bright light, hardly any shadows)
                            center  = (0, 0, 0),                                          # location at which the camera looks
#                            forward = (0, 0, -1),                                         # camera direction
                            range   = 10                                                  # zoom to the location
                          )
        scene.infoLabel = vs.label( pos = vs.vector(-5.5, 5.5, 0),
                                    border = 1,
                                    box = 0,
                                    opacity = 0,
                                    text = "",
                                    visible = False
                                  )

        # Assign to window
        self.scene = scene

        # Event handler
        self.scene.bind('click', self.OnClick)

    # EVENTS
    def OnClick(self, e):
        scene = self.scene
        scene.center = scene.mouse.pos # focus camera on new position
