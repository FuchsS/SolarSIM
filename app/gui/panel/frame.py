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
import controls.panel        as cp      # for the control panel
import controls.statusbar    as sb      # for the status bar
from simulation import Simulation           # for the simulation
from helpers.namer import fn_namer

from constants import *
    

import random
class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, init=50):
        self.data = self.init = init
        
    def next(self):
        self._recalc_data()
        return self.data
    
    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8: 
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta




class Window(wx.Frame):
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
    def __init__(self, parent, id, title, width, height):
        
        wx.Frame.__init__(self, parent, id, title, wx.Point(0, 0), wx.Size(width, height))
        self.SetIcon( wx.Icon('icons/title.png', wx.BITMAP_TYPE_PNG) ) # set application icon
        self.Maximize(True) # show full screen
        
        self.datagen = DataGen()
#        self.data1 = [self.datagen.next()]
        self.data1 = []
        data = []
        data2 = []
        for lat in LATS:
            data.append( (lat, 0) )
            data2.append( (lat, 0) )
        self.data2 = [data, data2]
#        self.data2 = [ -self.data1[-1] ]
                    
        # Create the panel, sizer and controls
        mb.MenuBar(self)
        self.toolbar      = tb.CreateToolBar(self)
        self.statusBar    = sb.CreateStatusBar(self)
        self.panel        = cp.CreatePanel(self, width, height)

        # Close all windows on exit
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def draw(self):
        self.chart1.drawPlot()
        self.chart2.drawPlot()

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
        options = self.panel.stepSize_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.stepSize     = getattr(self, 'stepSize', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
        # Simulation speed
        options = self.panel.speed_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.speed        = getattr(self, 'speed', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
        
        # READ ORBITAL SETTINGS
        # Eccentricity            
        options = self.panel.eccentricity_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.eccentricity = getattr(self, 'eccentricity', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
#            button.Disable() # BUG: If all radio buttons are disabled, then the value of the last option is always selected (since disabling triggers the event wx.EVT_RADIOBUTTON)
        # Tilt
        options = self.panel.tilt_options
        for button, label, value in options:
            if( button.GetValue() ):
                self.tilt         = getattr(self, 'tilt', value) # If the attribute does not exist yet, then a default value is returned, otherwise the current value.
#            button.Disable() # BUG: If all radio buttons are disabled, then the value of the last option is always selected (since disabling triggers the event wx.EVT_RADIOBUTTON)
        # Precession
        options = self.panel.precession_options
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
        options = self.panel.eccentricity_options
        for button, label, value in options:
            button.Enable()
        # Tilt
        options = self.panel.tilt_options
        for button, label, value in options:
            button.Enable()
        # Precession
        options = self.panel.precession_options
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
        options = self.panel.stepSize_options
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
        options = self.panel.speed_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• speed: {}".format( "{}x".format(value) ) )
                self.speed = value
                self.panel.speed.SetLabel( "{}x".format(value) )
                self.panel.speedSlider.SetValue( value )
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
        self.panel.speed.SetLabel( "{}x".format(value) )
        try:
            self.simulation.ChangeSimulationSpeed( value )
        except AttributeError:
            pass
    

    @fn_namer
    def OnSelectEccentricity(self, event):
        options = self.panel.eccentricity_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• eccentricity: {:f}".format(value).rstrip('0') )
                self.eccentricity = value
                self.panel.eccentricity.SetLabel( "{:f}".format(value).rstrip('0') )
#                try:
#                    self.simulation.ChangeOrbitalParameters( eccentricity=value )
#                except AttributeError:
#                    pass
    
    
    @fn_namer
    def OnSelectTilt(self, event):
        options = self.panel.tilt_options
        for button, label, value in options:
            if( button.GetValue() ): # Get the option, where radio button is checked
                print( "• tilt: {:.2f}°".format(value) )
                self.tilt = value
                self.panel.tilt.SetLabel( "{:.2f}".format(value) + unicode('°', 'utf-8') )
#                try:
#                    self.simulation.ChangeOrbitalParameters( tilt=value )
#                except AttributeError:
#                    pass
   
    
    @fn_namer
    def OnSelectPrecession(self, event):
        options = self.panel.precession_options
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
    def OnSave(self, event):
#        file_choices = "PNG (*.png)|*.png"
        
#        dlg = wx.FileDialog(
#            self.parent,
#            message     = "Save plot as...",
#            defaultDir  = os.getcwd(),
#            defaultFile = "plot.png",
#            wildcard    = file_choices,
#            style       = wx.SAVE
#        )
        dialog = wx.DirDialog (None, "Save in directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            file1 = self.chart1.title
            file2 = self.chart2.title
            self.chart1.canvas.print_figure(path + "\\" + file1, dpi=self.chart1.dpi)
            self.chart2.canvas.print_figure(path + "\\" + file2, dpi=self.chart2.dpi)
#            self.flash_status_message("Saved to %s" % path)
#        self.chart1.on_save_plot("Save")
#        self.chart2.on_save_plot("Save")

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