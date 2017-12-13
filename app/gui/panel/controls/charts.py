# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:56:47 2017

@author: Stefan
"""
import wx

# The recommended way to use wx with mpl is with the WXAgg backend.
import matplotlib
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import numpy as np
import pylab

class LineChart:
    
    def __init__(self, parent, data, title, xlabel, ylabel, xmin=None, xmax=None, ymin=None, ymax=None, xticks=None, yticks=None, showGrid=False):
        self.panel    = parent
        self.data     = data
        self.title    = title
        self.xlabel   = xlabel
        self.ylabel   = ylabel
        self.xmin     = xmin
        self.xmax     = xmax
        self.ymin     = ymin
        self.ymax     = ymax
        self.xticks   = xticks
        self.yticks   = yticks
        self.showGrid = showGrid
        
        self.createChart()
        

    def createChart(self):
        """
        Creates the chart.
        """
        self.dpi = 100
        width  = self.panel.GetSize()[0] * 0.01041666666667 # covert pixels to inches
        height = self.panel.GetSize()[1] * 0.01041666666667
        margin = 0.4
        
        self.fig  = plt.figure( figsize=(width, height-margin), dpi=self.dpi )
        self.axes = self.fig.add_subplot(111)
        self.axes.set_title(  self.title,  size=12)
        self.axes.set_xlabel( self.xlabel, size=8)
        self.axes.set_ylabel( self.ylabel, size=8)
        self.axes.tick_params(axis='both', which='major', labelsize=8) # set the font size of the ticks
        self.axes.set_axis_bgcolor('black')

        # Plot the data and save the reference
        self.plottedData = self.axes.plot(
            self.data,
            linewidth = 1,
            color     = (1, 1, 0),
        )[0]
        
        self.canvas = FigCanvas(self.panel, wx.ID_ANY, self.fig)
        
        self.drawPlot()
            
    
    def drawPlot(self):
        """
        Redraws the plot.
        """
        # 1. Determine xmin, xmax:
        #    If xmin is not set, it "follows" xmax to produce a sliding effect. 
        #    Therefore, xmin is assigned after xmax.
        if not self.xmax:
            xmax = len(self.data) if len(self.data) > 50 else 50
        else:
            xmax = self.xmax
        
        if not self.xmin:
            xmin = xmax - 50
        else:
            xmin = self.xmin
        
        # 2. Determine ymin, ymax:
        #    Find the min and max values of the data set and add a margin.
        if not self.ymin:
            ymin = round(min(self.data), 0) - 1
        else:
            ymin = self.ymin
        
        if not self.ymax:
            ymax = round(max(self.data), 0) + 1
        else:
            ymax = self.ymax

        self.axes.set_xbound( lower=xmin, upper=xmax )
        self.axes.set_ybound( lower=ymin, upper=ymax )
        
        # 3. Add ticks to the plot
        if self.xticks:
            self.axes.set_xticks( self.xticks )
        if self.yticks:
            self.axes.set_yticks( self.yticks )
        
        # 4. Add a grid to the chart
        if self.showGrid:
            self.axes.grid( True, color='gray' )
        else:
            self.axes.grid( False )
    
        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly 
        # iterate, and setp already handles this.
        #  
        pylab.setp(self.axes.get_xticklabels(), visible=True)
        
        self.plottedData.set_xdata( np.arange(len(self.data)) )
        self.plottedData.set_ydata( np.array(self.data) )
        
        self.canvas.draw()