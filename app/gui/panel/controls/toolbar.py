# -*- coding: utf-8 -*-

#############################
# Module:   ToolBar
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
    
    Contains the toolbar
    
"""

import wx # for widgets

class ToolBar:
    """ 
        ...
        
    """
    
    # CONSTRUCTOR
    def __init__(self, window):

        self.window = window
        toolbar  = self.window.CreateToolBar( style=( wx.TB_HORZ_LAYOUT | wx.TB_TEXT ) )

#        self.CreateItem( toolbar=toolbar, id=wx.ID_EXIT, name='&Quit', icon='icons/exit.png', event=self.window.OnQuit)
#        toolbar.AddSeparator()
#        self.CreateItem( toolbar=toolbar, id=wx.ID_NEW,  name='&New',  icon='icons/new.png',  event=self.window.OnNew , info='New simulation run')
#        self.CreateItem( toolbar=toolbar, id=wx.ID_OPEN, name='&Open', icon='icons/open.png', event=self.window.OnOpen, info="Open saved settings")
#        self.CreateItem( toolbar=toolbar, id=wx.ID_SAVE, name='&Save', icon='icons/save.png', event=self.window.OnSave, info="Save current settings")
        self.CreateItem( toolbar=toolbar, id=wx.ID_ANY, name='&Start', icon='icons/start.png', event=self.window.OnStart, info='Start simulation')
#        self.CreateItem( toolbar=toolbar, id=1000, name='&Pause', icon='icons/pause.png', event=self.window.OnPause, info='Pause simulation')
        self.CreateItem( toolbar=toolbar, id=wx.ID_ANY, name='&Stop' , icon='icons/stop.png',  event=self.window.OnStop , info='Stop simulation')
        toolbar.Realize()

        # Assign to window
        self.window.toolbar = toolbar

        

    # CREATE STANDARD ITEM
    def CreateItem(self, toolbar, id, name, icon, event, info=None):

        item = toolbar.AddLabelTool( id=id, label=name, bitmap=wx.Bitmap( icon ) )
##        if info:
##            item.SetHelp( info )
        self.window.Bind( wx.EVT_TOOL, event, item )
