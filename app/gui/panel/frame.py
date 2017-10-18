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

        self.SetSize((400, 800))
        self.SetTitle('SolarSIM')
        self.Centre()
        self.Show()



    # EVENTS AND FUNCTIONS
    def SetRotationRate(self, e, slideBar): # called on slider events
        self.simulation.ChangeSimulationSpeed( slideBar.GetValue()*5 )


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
