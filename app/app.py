# -*- coding: utf-8 -*-

#############################
# Module:   Simulation
# Author:   S.Fuchs
# Date:     2016/07/05
# Version:  Entwurf 0.1
#
# Beschreibung: Hauptprogramm
#
###############################
# Log:
# 2016/07/05    SF - Datei erzeugt
################################
""" Description:
    
    Contains the main program
    
"""

import wx                                   # for widgets

from simulation import Simulation           # for the simulation
from gui.animation.scene import Scene       # for the animation
from gui.panel.frame import ControlPanel    # for the control panel

class App:
  
    def __init__(self, *args, **kwargs):

        simulation = Simulation()
        animation  = Scene()
        panel      = ControlPanel( simulation )
        
        simulation.run( animation, panel )
    
def main():
    app = wx.App()
    App()
    app.MainLoop() 

if __name__ == '__main__':
    main()
