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
width  = 400
height = 400
cols = range(20, width,  10)  # Set of columns to align labels and buttons
rows = range(20, height, 20)  # Set of rows



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
        
        """
            Set the font with wx.Font:
            wx.Font(
                pointSize,
                family,
                style,
                weight,
                underline=False,
                faceName="",
                encoding=wx.FONTENCODING_DEFAULT
            )
            family can be: wx.DECORATIVE, wx.DEFAULT,wx.MODERN, wx.ROMAN, wx.SCRIPT or wx.SWISS.
            style  can be: wx.NORMAL, wx.SLANT or wx.ITALIC.
            weight can be: wx.NORMAL, wx.LIGHT or wx.BOLD.
        """
        h1 = wx.Font( pointSize=12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.BOLD  , underline=False )
        h2 = wx.Font( pointSize=10, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=True )
        normal = wx.Font( pointSize=10, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL, underline=False )
        
# TO DO: replace index of row throug a row.next()
        # Title
        wx.StaticText( parent=controlPanel, label='General settings', 
                      pos=(cols[0], rows[0]) ).SetFont( h1 )         
        
        # SETTINGS: SIMULATION SPEED
        # Selection of the simulation step size
        wx.StaticBox( parent=controlPanel, label='Simulation step',
                     pos=(cols[0], rows[2]), size=(200, 80) )
        stepSizes = [('every hour', 3600), ('every day', 86400)]
        i = 3
        for label, value in stepSizes:
            if (i == 3):
                wx.RadioButton( parent=controlPanel, label=label,
                               pos=(cols[1], rows[i]), style=wx.RB_GROUP)
            else:
                wx.RadioButton( parent=controlPanel, label=label,
                               pos=(cols[1], rows[i]))
            i=i+1
#        wx.RadioButton( parent=controlPanel, label='every hour',
#                       pos=(cols[1], rows[3]), style=wx.RB_GROUP)
#        wx.RadioButton( parent=controlPanel, label='every day',
#                       pos=(cols[1], rows[4]))
        self.window.Bind( wx.EVT_RADIOBUTTON, self.window.OnSelectStepsize)
        controlPanel.stepSizes = stepSizes
        
        # Selection of the simulation speed
        wx.StaticBox(   parent=controlPanel, label='Simulation speed',
                       pos=(cols[0], rows[7]), size=(200, 160))
        speedOptions = [('1x', 1), ('5x', 5), ('10x', 10), ('25x', 25),
                         ('50x', 50), ('100x', 100)]
        i = 8
        for label, value in speedOptions:
            if (i == 8):
                wx.RadioButton( parent=controlPanel, label=label,
                               pos=(cols[1], rows[i]), style=wx.RB_GROUP)
            else:
                wx.RadioButton( parent=controlPanel, label=label,
                               pos=(cols[1], rows[i]))
            i=i+1
        self.window.Bind( wx.EVT_RADIOBUTTON, self.window.OnSelectSpeed )
        controlPanel.speedOptions = speedOptions
        
        # Slider to control the speed of the simulation
        controlPanel.slider = wx.Slider( parent=controlPanel, value=1, minValue=1, maxValue=100, 
                  pos=(cols[16], rows[8]), size=(-1, 140), 
                  style=(wx.SL_LEFT | wx.SL_INVERSE | wx.SL_MIN_MAX_LABELS ) )
        self.window.Bind( wx.EVT_SCROLL, self.window.OnSliderScroll )
        
        # Display the current value
        controlPanel.speed = wx.StaticText( parent=controlPanel, label='1x', 
                                   pos=(cols[13], rows[11])) 

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
