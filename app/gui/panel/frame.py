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
import visual as vs
import wx                   # for widgets

import controls.menubar   as mb      # for the menu bar
import controls.toolbar   as tb      # for the toolbar
import controls.sidepanel as sp      # for the side panel
import controls.statusbar as sb      # for the status bar
from simulation import Simulation           # for the simulation
from gui.animation.scene import Scene       # for the animation
import time
import multiprocessing

class ControlPanel(wx.Frame):
    """ Beschreibung:
        
        Diese Klasse enthält alle UI-Elemente.
        
    """
    
    # CONSTRUCTOR
    def __init__(self,  *args, **kwargs):
        wx.Frame.__init__(self, None)
#        self.simulation = simulation
#        self.animation  = animation

        mb.MenuBar(self)
        tb.ToolBar(self)
        sb.StatusBar(self)
        sp.SidePanel(self)

        self.SetTitle('SolarSIM') # set the title of the frame
        self.SetSize((400, 800)) # set the default size of the window
#        self.Maximize(True) # maximize the frame
#        self.Centre() # center the window
        self.SetPosition((0,0)) # set a specific position on the screen
        self.SetIcon( wx.Icon('icons/title.png', wx.BITMAP_TYPE_PNG) ) # set application icon
        self.Show(True) # display the window
        
        # CLOSE ALL WINDOWS ON EXIT
        self.Bind(wx.EVT_CLOSE, self.OnQuit)


    # EVENTS AND FUNCTIONS
    def OnSelectStepsize(self, event):
        obj = event.GetEventObject()
        options = self.sidePanel.controlPanel.stepSize_options
        for label, value in options:
            if(label == obj.GetLabel()):
                print label
                self.simulation.ChangeSimulationStepsize( value )
    
    def OnSelectSpeed(self, event): 
        obj = event.GetEventObject()
        options = self.sidePanel.controlPanel.speed_options
        for label, value in options:
            if(label == obj.GetLabel()):
                print label
                self.simulation.ChangeSimulationSpeed( value )
                self.sidePanel.controlPanel.speed.SetLabel( "{}x".format(value) )
                self.sidePanel.controlPanel.slider.SetValue( value )
     
    def OnSelectEccentricity(self, e): 
        obj = e.GetEventObject()
        options = self.sidePanel.controlPanel.eccentricity_options
        for label, value in options:
            if(label == obj.GetLabel()):
                print label
                self.simulation.ChangeOrbitalParameters( eccentricity=value )
                self.sidePanel.controlPanel.eccentricity.SetLabel( "{:.5f}".format(value) )
                
    def OnSelectTilt(self, e): 
        obj = e.GetEventObject()
        options = self.sidePanel.controlPanel.tilt_options
        for label, value in options:
            if(label == obj.GetLabel()):
                print label
                self.simulation.ChangeOrbitalParameters( tilt=value )
                self.sidePanel.controlPanel.tilt.SetLabel( "{:.2f}".format(value) + unicode('°', 'utf-8') )
    
    def OnSelectPrecession(self, e): 
        obj = e.GetEventObject()
        options = self.sidePanel.controlPanel.precession_options
        for label, value in options:
            if(label == obj.GetLabel()):
                print value
                self.simulation.ChangeOrbitalParameters( precession=value )
    
    def OnSliderScroll(self, event): # called on slider events
        obj   = event.GetEventObject()
        value = obj.GetValue()
        self.simulation.ChangeSimulationSpeed( value )
        self.sidePanel.controlPanel.speed.SetLabel( "{}x".format(value) )


    def OnStart(self, event):
        self.animation  = Scene()
        self.simulation = Simulation()
        self.simulation.run(self.animation, self)
                

    def OnStop(self, event):
        try:
            self.simulation.stop()        
        except AttributeError:
            pass
# Bug!!!         
#        # Close any opened scence
#        try:
#            self.animation.scene.delete()
#        except AttributeError:
#            pass
    
            
    def OnQuit(self, event):
        try:
            self.OnStop(wx.EVT_CLOSE);
        except AttributeError:
            pass
        try:
            if (self.simulation.isStopped == True):
                wx.Exit()
        except AttributeError:
            wx.Exit()


    def OnAbout(self, event):
    	pass
    	

    def OnHelp(self, event):
        pass
    

    def ToggleStatusbar(self, e):
        if self.showStatusbar.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()


    def ToggleToolbar(self, e):
        if self.showToolbar.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()
