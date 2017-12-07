# -*- coding: utf-8 -*-

#############################
# Module:   GUI
# Author:   S.Fuchs
# Date:     2016/07/05
# Version:  Entwurf 0.1
#
# Beschreibung: GUI
#
###############################
# Log:
# 2016/07/05    SF - Datei erzeugt
################################
""" Description:
    
    Contains the UI
    
"""
import wx # for widgets

import controls.menubar      as mb      # for the menu bar
import controls.toolbar      as tb      # for the toolbar
import controls.controlpanel as cp      # for the dontrol panel
import controls.statusbar    as sb      # for the status bar
from simulation import Simulation           # for the simulation
from helpers.namer import fn_namer
    

class ControlWindow(wx.Frame):
    """
    Construct a wx.Frame object.

    __init__ (self, parent, id=ID_ANY, title=””, pos=DefaultPosition, size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
    
    Parameters:

        parent (wx.Window) – The window parent. This may be, and often is, None. If it is not None, the frame will be minimized when its parent is minimized and restored when it is restored (although it will still be possible to minimize and restore just this frame itself).
        id (wx.WindowID)   – The window identifier. It may take a value of -1 to indicate a default value.
        title (string)     – The caption to be displayed on the frame’s title bar.
        pos (wx.Point)     – The window position. The value DefaultPosition indicates a default position, chosen by either the windowing system or wxWidgets, depending on platform.
        size (wx.Size)     – The window size. The value DefaultSize indicates a default size, chosen by either the windowing system or wxWidgets, depending on platform.
        style (long)       – The window style. See wx.Frame class description.
        name (string)      – The name of the window. This parameter is used to associate a name with the item, allowing the application user to set Motif resource values for individual windows.
    """
    # CONSTRUCTOR
    def __init__(self, parent, id, title):
        
        wx.Frame.__init__(self, parent, id, title, wx.Point(0, 0), wx.Size(400, 800))
        self.SetIcon( wx.Icon('icons/title.png', wx.BITMAP_TYPE_PNG) ) # set application icon
        
        # Create the panel, sizer and controls
        mb.MenuBar(self)
        self.toolbar      = tb.CreateToolBar(self)
        self.statusBar    = sb.CreateStatusBar(self)
        self.controlPanel = cp.CreateControlPanel(self)

        # Close all windows on exit
        self.Bind(wx.EVT_CLOSE, self.OnClose)        

#------------------------------------------------------------------------------

    @fn_namer
    def OnStart(self, event):
        """
        Start the simulation.
        """
        # Enables/disables buttons
        startButtonId = self.toolbar.startButton.GetId()
        stopButtonId  = self.toolbar.stopButton.GetId()
        self.toolbar.EnableTool(startButtonId, False)
        self.toolbar.EnableTool(stopButtonId, True)
            
        # READ SIMULATION SETTINGS
        # Simulation step size
        options = self.controlPanel.stepSize_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.stepSize     = getattr(self, 'stepSize', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
        # Simulation speed
        options = self.controlPanel.speed_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.speed        = getattr(self, 'speed', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
        
        # READ ORBITAL SETTINGS
        # Eccentricity            
        options = self.controlPanel.eccentricity_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.eccentricity = getattr(self, 'eccentricity', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
#            button.Disable() # BUG: If all radio buttons are disabled, then the value of the last option is always selected (since disabling triggers the event wx.EVT_RADIOBUTTON)
        # Tilt
        options = self.controlPanel.tilt_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.tilt         = getattr(self, 'tilt', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
#            button.Disable() # BUG: If all radio buttons are disabled, then the value of the last option is always selected (since disabling triggers the event wx.EVT_RADIOBUTTON)
        # Precession
        options = self.controlPanel.precession_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.precession   = getattr(self, 'precession', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
#            button.Disable() # BUG: If all radio buttons are disabled, then the value of the last option is always selected (since disabling triggers the event wx.EVT_RADIOBUTTON)
                
        # Starts the simulation with the selected settings
        self.simulation = Simulation(self, self.stepSize, self.speed, self.eccentricity, self.tilt, self.precession) # Creates a new simulation instance
        self.simulation.runSimulation() # Starts the simulation


    @fn_namer
    def OnStop(self, event):
        """
        Stop the simulation.
        """
        # Enables/disables buttons
        startButtonId = self.toolbar.startButton.GetId()
        stopButtonId  = self.toolbar.stopButton.GetId()
        self.toolbar.EnableTool(startButtonId, True)
        self.toolbar.EnableTool(stopButtonId, False)
        # Eccentricity
        options = self.controlPanel.eccentricity_options
        for button, label, value in options:
            button.Enable()
        # Tilt
        options = self.controlPanel.tilt_options
        for button, label, value in options:
            button.Enable()
        # Precession
        options = self.controlPanel.precession_options
        for button, label, value in options:
            button.Enable()
        
        # Stops the simulation
        try:
            self.simulation.stopSimulation()
        except AttributeError:
            pass


    @fn_namer
    def OnClose(self, event):
        """
        Close the app.
        """
        try:
            if(self.simulation.isStopped):
                wx.Exit()
            else:
                self.OnStop(wx.EVT_CLOSE);
        except AttributeError:
            wx.Exit()

#------------------------------------------------------------------------------

    # CHANGE OF SIMULATION SETTINGS
    @fn_namer
    def OnSelectStepsize(self, event):
        options = self.controlPanel.stepSize_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• stepSize: {} seconds".format( value ) )
                self.stepSize = value
                try:
                    self.simulation.ChangeSimulationStepsize( value )
                except AttributeError:
                    pass
    
    
    @fn_namer
    def OnSelectSpeed(self, event): 
        options = self.controlPanel.speed_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• speed: {}".format( "{}x".format(value) ) )
                self.speed = value
                self.controlPanel.speed.SetLabel( "{}x".format(value) )
                self.controlPanel.speedSlider.SetValue( value )
                try:
                    self.simulation.ChangeSimulationSpeed( value )
                except AttributeError:
                    pass
                
    
    @fn_namer
    def OnSpeedSlider(self, event): # called on slider events
        obj   = event.GetEventObject()
        value = obj.GetValue()
        print( "• speed: {}".format( "{}x".format(value) ) )
        self.speed = value
        self.controlPanel.speed.SetLabel( "{}x".format(value) )
        try:
            self.simulation.ChangeSimulationSpeed( value )
        except AttributeError:
            pass
    

    @fn_namer
    def OnSelectEccentricity(self, event):
        options = self.controlPanel.eccentricity_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• eccentricity: {:f}".format(value).rstrip('0') )
                self.eccentricity = value
                self.controlPanel.eccentricity.SetLabel( "{:f}".format(value).rstrip('0') )
#                try:
#                    self.simulation.ChangeOrbitalParameters( eccentricity=value )
#                except AttributeError:
#                    pass
    
    
    @fn_namer
    def OnSelectTilt(self, event):
        options = self.controlPanel.tilt_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• tilt: {:.2f}°".format(value) )
                self.tilt = value
                self.controlPanel.tilt.SetLabel( "{:.2f}".format(value) + unicode('°', 'utf-8') )
#                try:
#                    self.simulation.ChangeOrbitalParameters( tilt=value )
#                except AttributeError:
#                    pass
   
    
    @fn_namer
    def OnSelectPrecession(self, event):
        options = self.controlPanel.precession_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• tilt: {}".format(value) )
                self.precession = value
#                try:
#                    self.simulation.ChangeOrbitalParameters( precession=value )
#                except AttributeError:
#                    pass
    
#------------------------------------------------------------------------------

    @fn_namer
    def OnAbout(self, event):
    	pass
    	
    
    @fn_namer
    def OnHelp(self, event):
        pass
    
       
    @fn_namer
    def ToggleStatusbar(self, e):
        if self.showStatusbar.IsChecked():
            self.statusBar.Show()
        else:
            self.statusBar.Hide()

       
    @fn_namer
    def ToggleToolbar(self, e):
        if self.showToolbar.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()
