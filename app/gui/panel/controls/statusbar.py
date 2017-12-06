# -*- coding: utf-8 -*-

def CreateStatusBar(self):
    """ 
    Creates the status bar.
    
    Creates a wx.StatusBar for a wx.Frame.
    
    Parameters:
        
        self    - wx.Frame
        
    """
    # Get a new toolbar instance
    statusBar = self.CreateStatusBar()
    statusBar.SetStatusText('Ready')
    
    return statusBar
