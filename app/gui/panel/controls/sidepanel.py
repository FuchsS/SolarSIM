# -*- coding: utf-8 -*-

#############################
# Module:   SidePanel
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
    
    Contains the side panel
    
"""

import wx # for widgets



# globals
cols = range(20, 500, 120)  # Set of columns to align labels and buttons
rows = range(10, 250,  30)  # Set of rows
width  = 400
height = 400



class SidePanel:
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__(self, window):

        self.window    = window
        self.sidePanel = wx.Panel( parent=self.window )
        
        # Assign panels to side panel
        self.sidePanel.controlPanel = self._init_controlPanel()
        self.sidePanel.infoPanel    = self._init_infoPanel()

        # Assign to window
        self.window.sidePanel       = self.sidePanel



    # CONTROL PANEL
    def _init_controlPanel(self):
        controlPanel = wx.Panel( parent=self.window, pos=(0, 0), size=(width, height) )
        
        # SPEED, slider to control the speed of the simulation
        sliderPanel=wx.StaticText( parent=controlPanel, pos=(cols[0], rows[0]), label='Speed:' )
        slider=wx.Slider( parent=controlPanel, pos=(cols[1], rows[0]), minValue=0, maxValue=100 )
        slider.SetValue(10)
        self.window.Bind( wx.EVT_SCROLL, lambda event: self.window.SetRotationRate(event, slider), slider )

        return controlPanel      



    # INFO PANEL
    def _init_infoPanel(self):
        infoPanel = wx.Panel( parent=self.window, pos=(0, height), size=(width, height), style=wx.BORDER )

        infoPanel.time               = self.CreateItem( panel=infoPanel, label='Time:',                value='', row=0 )
        infoPanel.distance           = self.CreateItem( panel=infoPanel, label='Distance:',            value='', row=1 )
        infoPanel.orbitalVelocity    = self.CreateItem( panel=infoPanel, label='Orbital velocity:',    value='', row=2 )
        infoPanel.rotationalVelocity = self.CreateItem( panel=infoPanel, label='Rotational velocity:', value='', row=3 )

        return infoPanel     



    # CREATE STANDARD ITEM
    def CreateItem(self, panel, label, value, row):

        itemLabel = wx.StaticText( parent=panel, label=label, pos=(cols[0], rows[row]) )
        itemValue = wx.StaticText( parent=panel, label=value, pos=(cols[1], rows[row]) )

        return itemValue
