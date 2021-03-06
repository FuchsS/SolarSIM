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
""" Description: Contains the side panel
    
"""

import wx # for widgets


import charts
from constants import *


# CONTROL PANEL
def CreatePanel(self, width, height):
    """
    create main panel with controls and charts
    """
# TO DO: Create a class with radio buttons, which have a return value
    mainPanel = wx.Panel( parent=self, pos=(0, 0), size=(width, height) )
    
    cols = range(20, width,  10)  # Set of columns to align labels and buttons
    rows = range(20, height, 20)  # Set of rows
    row = iter(rows)
    border = 20
    margin = 20
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
    
    # CHART REGION
    chartRegion = wx.Panel(mainPanel, pos=(width/3, 0), size=(width, height-border), style=wx.SIMPLE_BORDER)
    # Title
    wx.StaticText( parent=chartRegion, id=wx.NewId(), label='SOLAR RADIATION', 
                   pos=(0, 0)
                 ).SetFont( h1 )
    # First chart
    xmin=0
    xmax=365
    xsteps=50
    ymin=-90
    ymax=90
    ysteps=30
    chartPanel1 = wx.Panel(chartRegion, pos=(0, margin), size=(width, height/2))
    self.chart1 = charts.HeatMap(
        parent  = chartPanel1,
        data    = self.data1,
        title   = "Solar Radiation - Distribution Over Seasons And Latitudes",
        xlabel  = "Day",
        ylabel  = "Latitude",
        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
        xticks=range(xmin, xmax+1, xsteps), yticks=range(ymin, ymax+1, ysteps),
        showGrid=True,
    )
    # Second chart
    xmin=-90
    xmax=90
    xsteps=30
    ymin=150
    ymax=450
    ysteps=50
    chartPanel2 = wx.Panel(chartRegion, pos=(0, height/2), size=(width, height/2))
    self.chart2 = charts.LineChart(
        parent  = chartPanel2,
        data    = self.data2,
        title   = "Solar Radiation - Annual Average Distribution Over Latitudes",
        xlabel  = "Latitude",
        ylabel  = u"Medium zonal solar radiation (W/m²)",
        xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax,
        xticks=range(xmin, xmax+1, xsteps), yticks=range(ymin, ymax+1, ysteps),
        labels=['Settings','Today\'s conditions'],
        showGrid=True,
    )
    
    
    # GENERAL SETTINGS
    # Title
    wx.StaticText( parent=mainPanel, id=wx.NewId(), label='General settings', 
                   pos=( cols[0], row.next() )
                 ).SetFont( h1 )
    
    # Skip one line
    row.next()
    
    # SELECTION OF THE SIMULATION STEP SIZE
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Live drawing',
                  pos=( cols[0], row.next() ), size=(200, 80)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="yes", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="no")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectLiveDrawing, radio )
    options = [ (radio1, radio1.GetLabel(), True), (radio2, radio2.GetLabel(), False) ]
    mainPanel.liveDrawing_options = options
    mainPanel.liveDrawing_radioButtons = radioButtons
    
    # Skip two lines
    row.next()
    row.next()
    
    # SELECTION OF THE SIMULATION STEP SIZE
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Simulation step',
                  pos=( cols[0], row.next() ), size=(200, 80)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="every hour", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="every day")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectStepsize, radio )
    options = [ (radio1, radio1.GetLabel(), 3600), (radio2, radio2.GetLabel(), 86400) ]
    mainPanel.stepSize_options = options
    mainPanel.stepSize_radioButtons = radioButtons
    
    # Skip two lines
    row.next()
    row.next()
    
    # SELECTION OF THE SIMULATION SPEED   
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Simulation speed',
                  pos=( cols[0], row.next() ), size=(200, 160)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="1x", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="5x")
    radio3 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="10x")
    radio4 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="25x")
    radio5 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="50x")
    radio6 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="100x")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    radioButtons.append(radio3)
    radioButtons.append(radio4)
    radioButtons.append(radio5)
    radioButtons.append(radio6)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectSpeed, radio )
    options = [ (radio1, radio1.GetLabel(), 1),
                (radio2, radio2.GetLabel(), 5),
                (radio3, radio3.GetLabel(), 10),
                (radio4, radio4.GetLabel(), 25),
                (radio5, radio5.GetLabel(), 50),
                (radio6, radio6.GetLabel(), 100),
              ]
    mainPanel.speed_options = options
      
    # Slider to control the speed of the simulation
    mainPanel.speedSlider = wx.Slider( parent=mainPanel, id=wx.NewId(), value=1, minValue=1, maxValue=100, 
              pos=(cols[16], rows[13]), size=(-1, 140), 
              style=(wx.SL_LEFT | wx.SL_INVERSE | wx.SL_MIN_MAX_LABELS ) )
    self.Bind( wx.EVT_SCROLL, self.OnSpeedSlider )
    
    # Display the current value
    mainPanel.speed = wx.StaticText( parent=mainPanel, id=wx.NewId(), label='1x', 
                               pos=(cols[13], rows[16]))
    
    # Skip two lines
    row.next()
    row.next()

    # ORBITAL SETTINGS
    # Title
    wx.StaticText( parent=mainPanel, id=wx.NewId(), label='Orbital settings', 
                   pos=( cols[0], row.next() )
                 ).SetFont( h1 )
    
    # Skip one line
    row.next()
    
    # SELECTION OF THE ECCENTRICITY
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Eccentricity',
                  pos=( cols[0], row.next() ), size=(200, 80)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="today", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="min")
    radio3 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="max")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    radioButtons.append(radio3)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectEccentricity, radio )
    options = [ (radio1, radio1.GetLabel(), 0.0167086),
                (radio2, radio2.GetLabel(), 0.000055),
                (radio3, radio3.GetLabel(), 0.0679),
              ]
    mainPanel.eccentricity_options = options
    
    # Display the current value
    mainPanel.eccentricity = wx.StaticText( parent=mainPanel, id=wx.NewId(), label='0.01671', 
                               pos=(cols[13], rows[25]))
    
    # Skip one line
    row.next()
    
    # SELECTION OF THE AXIAL TILT
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Axial tilt',
                  pos=( cols[0], row.next() ), size=(200, 80)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="today", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="min")
    radio3 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="max")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    radioButtons.append(radio3)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectTilt, radio )
    options = [ (radio1, radio1.GetLabel(), 23.44),
                (radio2, radio2.GetLabel(), 22.1),
                (radio3, radio3.GetLabel(), 24.5),
              ]
    mainPanel.tilt_options = options
    
    # Display the current value
    mainPanel.tilt = wx.StaticText( parent=mainPanel, id=wx.NewId(), label='23.44'+unicode('°', 'utf-8'), 
                               pos=(cols[13], rows[30]))
    
    # Skip one line
    row.next()
    
    # SELECTION OF THE PRECESSION
    wx.StaticBox( parent=mainPanel, id=wx.NewId(), label='Axial precession',
                  pos=( cols[0], row.next() ), size=(200, 80)
                ).SetFont( normal )
    # Create a group of radio buttons
    radioButtons = []
    radio1 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="today", style=wx.RB_GROUP)
    radio2 = wx.RadioButton( parent=mainPanel, id=wx.NewId(), label="in about 13,000 years")
    radioButtons.append(radio1)
    radioButtons.append(radio2)
    # Set position for each radio button and setup an event handler
    for radio in radioButtons:
        radio.SetPosition( (cols[1], row.next() ) )
        self.Bind( wx.EVT_RADIOBUTTON, self.OnSelectPrecession, radio )
    options = [ (radio1, radio1.GetLabel(),  1),
                (radio2, radio2.GetLabel(), -1),
              ]
    mainPanel.precession_options = options


    return mainPanel
    