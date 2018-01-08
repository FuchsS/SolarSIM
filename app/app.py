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
    
    Contains the main program.
        Call sequence: App -> Window -> Menu
                                     -> Toolbar
                                     -> StatusBar
                                     -> MainPanel -> Chart1
                                                  -> Chart2
                                     -OnStart -> Simulation -> Model
                                                            -> Animation
                                     
    
"""

import wx                                   # for widgets
from   gui.panel.frame import Window # for the control window

class App(wx.App):
    """
    Initialise the App.
        
    __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True)
    
    Parameters:	

        redirect (bool)      – Should error messages (sys.stdout and sys.stderr) be redirected? Specify a filename to redirect the error messages to a file.
        filename (string)    – The name of a file to redirect output to, if redirect is True.
        useBestVisual (bool) – Should the app try to use the best available visual provided by the system (only relevant on systems that have more than one visual).
        clearSigInt (bool)   – Should SIGINT be cleared? This allows the app to terminate upon a Ctrl-C in the console like other GUI apps will.

    """
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect, filename, useBestVisual, clearSigInt)
        
        
    
    def OnInit(self):
        """
        Initialise the app with a control window.
        """
        self.frame = Window(None, id=wx.ID_ANY, title='SolarSIM', width=1024, height=768)
        self.frame.Show(True) # display the window
        return True

    
if __name__ == '__main__':     
    # Create the app
    app = App(redirect=False, filename='SolarSim.stderr.log')
    app.MainLoop()
    