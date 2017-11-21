# -*- coding: utf-8 -*-

#############################
# Module:   StatusBar
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
    
    Contains the statusbar
    
"""

import wx # for widgets

class StatusBar:
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__(self, window):

        self.window = window

        statusBar = self.window.CreateStatusBar()
        statusBar.SetStatusText('Ready')

        # Assign to window
        self.window.statusBar = statusBar
