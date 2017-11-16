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

import wx                   # for widgets

import controls.menubar   as mb      # for the menu bar
import controls.toolbar   as tb      # for the toolbar
import controls.sidepanel as sp      # for the side panel
import controls.statusbar as sb      # for the status bar

class ControlPanel(wx.Frame):
    """ Beschreibung:
        
        Diese Klasse enthält alle UI-Elemente.
        
    """
    
    # CONSTRUCTOR
    def __init__(self, simulation, *args, **kwargs):
        wx.Frame.__init__(self, None)
        self.simulation = simulation

        mb.MenuBar(self)
        tb.ToolBar(self)
        sb.StatusBar(self)
        sp.SidePanel(self)

        self.SetTitle('SolarSIM') # set the title of the frame
        self.Maximize(True) # maximize the frame
#        self.SetSize((800, 800)) # set the size of the window
#        self.Centre() # center the window
#        self.SetPosition((0,0)) # set a specific position on the screen
        self.SetIcon( wx.Icon('icons/title.png', wx.BITMAP_TYPE_PNG) ) # set application icon
        self.Show(True) # display the window
        
        # CLOSE ALL WINDOWS ON EXIT
        self.Bind(wx.EVT_CLOSE, self.OnQuit)



    # EVENTS AND FUNCTIONS
    def OnSelectStepsize(self, e):
        print e, 'test'
        obj = e.GetEventObject()
        stepSizes = self.sidePanel.controlPanel.stepSizes
        for label, value in stepSizes:
            if(label == obj.GetLabel()):
                print value,' is clicked from Radio Group'
#                self.simulation.ChangeSimulationSpeed( value )
#                self.sidePanel.controlPanel.speed.SetLabel( str(value) + "x" )
#                self.sidePanel.controlPanel.slider.SetValue( value )
    
    def OnSelectSpeed(self, e): 
        obj = e.GetEventObject()
        speedOptions = self.sidePanel.controlPanel.speedOptions
        for label, value in speedOptions:
            if(label == obj.GetLabel()):
                print value,' is clicked from Radio Group'
                self.simulation.ChangeSimulationSpeed( value )
                self.sidePanel.controlPanel.speed.SetLabel( str(value) + "x" )
                self.sidePanel.controlPanel.slider.SetValue( value )
      
    def OnSliderScroll(self, e): # called on slider events
        obj   = e.GetEventObject()
        value = obj.GetValue()
        self.simulation.ChangeSimulationSpeed( value )
        self.sidePanel.controlPanel.speed.SetLabel( str(value) + "x" )


    def OnNew(self):
        pass
        

    def OnOpen(self):
        pass

        
    def OnSave(self):
        pass
    
            
    def OnQuit(self, e):
        wx.Exit()


    def OnAbout(self):
    	pass
    	

    def OnHelp(self):
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
