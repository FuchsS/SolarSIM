# -*- coding: utf-8 -*-

#############################
# Module:   MenuBar
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
    
    Contains the menubar
    
"""

import wx # for widgets

class MenuBar:
    """ 
        We create a menubar for our window. Every menu has several menu items,
         which are created in 5 steps.
        
    """
    
    # CONSTRUCTOR
    def __init__(self, window):

        self.window = window
        menubar  = wx.MenuBar()

        # Assign menus to menubar
        menubar.Append(self._init_fileMenu(), '&File')
        menubar.Append(self._init_editMenu(), '&Edit')
        menubar.Append(self._init_viewMenu(), '&View')

        # Assign to window
        self.window.SetMenuBar(menubar)



    # FILE MENU
    def _init_fileMenu(self):
        fileMenu = wx.Menu()
        
#        self.CreateMenuItem( menu=fileMenu, id=wx.ID_NEW,  name='&New',  shortcut='Ctrl+N', icon='icons/new.png',  event=self.window.OnNew , info='New simulation run')
#        self.CreateMenuItem( menu=fileMenu, id=wx.ID_OPEN, name='&Open', shortcut='Ctrl+O', icon='icons/open.png', event=self.window.OnOpen, info="Open saved settings")
#        self.CreateMenuItem( menu=fileMenu, id=wx.ID_SAVE, name='&Save', shortcut='Ctrl+S', icon='icons/save.png', event=self.window.OnSave, info="Save current settings")
        fileMenu.AppendSeparator()
        self.CreateMenuItem( menu=fileMenu, id=wx.ID_EXIT, name='&Quit', shortcut='Ctrl+Q', icon='icons/exit.png', event=self.window.OnQuit)

        return fileMenu



    # EDIT MENU
    def _init_editMenu(self):
        editMenu = wx.Menu()

        importSubmenu = wx.Menu()
        importSubmenu.Append(wx.ID_ANY, 'Import css...')
        importSubmenu.Append(wx.ID_ANY, 'Import txt...')
        importSubmenu.Append(wx.ID_ANY, 'Import database...')
        editMenu.AppendMenu(wx.ID_ANY, 'I&mport', importSubmenu)
        
        return editMenu



    # VIEW MENU
    def _init_viewMenu(self):
        viewMenu = wx.Menu()

        self.window.showStatusbar = viewMenu.Append(wx.ID_ANY, 'Statusbar', 
            'Show/Hide Statusbar', kind=wx.ITEM_CHECK)
        self.window.showToolbar   = viewMenu.Append(wx.ID_ANY, 'Toolbar', 
            'Show/Hide Toolbar',   kind=wx.ITEM_CHECK)         
        viewMenu.Check(self.window.showStatusbar.GetId(), True)
        viewMenu.Check(self.window.showToolbar.GetId(),   True)
        self.window.Bind(wx.EVT_MENU, self.window.ToggleStatusbar, self.window.showStatusbar)
        self.window.Bind(wx.EVT_MENU, self.window.ToggleToolbar,   self.window.showToolbar)
        
        return viewMenu



    # CREATE STANDARD MENU ITEM
    def CreateMenuItem(self, menu, id, name, shortcut, icon, event, info=None):

        item = wx.MenuItem( parentMenu=menu, id=id, text=name + '\t' + shortcut)
        if info:
            item.SetHelp(info)
        item.SetBitmap( wx.Bitmap ( icon ) )
        self.window.Bind( wx.EVT_MENU, event, item )
        menu.AppendItem( item )
