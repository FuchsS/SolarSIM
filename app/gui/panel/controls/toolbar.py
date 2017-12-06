# -*- coding: utf-8 -*-

import wx # for widgets

def CreateToolBar(self):
    """ 
    Creates the tool bar.
    
    Creates a wx.ToolBar for a wx.Frame.
    
    Parameters:
        
        self    - wx.Frame
        
    """
    # Get a new toolbar instance
    toolbar = self.CreateToolBar()
    toolbar.SetToolBitmapSize( (24, 24) )
    
    # Creates a start button
    startIcon           = wx.Bitmap('icons/start.png')
    startButtonId       = wx.NewId()
    startButton         = toolbar.AddTool( startButtonId, startIcon )
    toolbar.startButton = startButton
    toolbar.EnableTool(startButtonId, True)
    
    toolbar.Bind( wx.EVT_TOOL, self.OnStart, startButton ) # Event when start button is pressed
    
    # Creates a stop button
    stopIcon            = wx.Bitmap('icons/stop.png')
    stopButtonId        = wx.NewId()
    stopButton          = toolbar.AddTool( stopButtonId, stopIcon )
    toolbar.stopButton  = stopButton
    toolbar.EnableTool(stopButtonId, False)
    
    toolbar.Bind( wx.EVT_TOOL, self.OnStop, stopButton ) # Event when stop button is pressed
    
    # Realize the toolbar
    toolbar.Realize()
    
    return toolbar
