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
    
    def __init__(self, parent, data, title, xlabel, ylabel, xmin=None, xmax=None, ymin=None, ymax=None, xticks=None, yticks=None, xticks_minor=None, yticks_minor=None, showGrid=False):
        self.panel        = parent
        self.data         = data
        self.title        = title
        self.xlabel       = xlabel
        self.ylabel       = ylabel
        self.xmin         = xmin
        self.xmax         = xmax
        self.ymin         = ymin
        self.ymax         = ymax
        self.xticks       = xticks
        self.xticks_minor = xticks_minor
        self.yticks       = yticks
        self.yticks_minor = yticks_minor
        self.showGrid     = showGrid
        
        self.plottedData = []
        
        self.createChart()
        

    def createChart(self):
        """
        Creates the chart.
        """
        self.dpi = 100
        width  = self.panel.GetSize()[0] * 0.01041666666667 # covert pixels to inches
        height = self.panel.GetSize()[1] * 0.01041666666667
        margin = 0.4
        
        self.fig = plt.figure( figsize=(width, height-margin), dpi=self.dpi )
        self.ax  = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title(  self.title,  size=12)
        self.ax.set_xlabel( self.xlabel, size=8)
        self.ax.set_ylabel( self.ylabel, size=8)
        self.ax.tick_params(axis='both', which='major', labelsize=8) # set the font size of the ticks
        self.ax.set_axis_bgcolor('black')

        colors = ['white', 'red', 'yellow', 'green']
        # Plot the data and save the reference
        for i, subplot in enumerate(self.data):
            self.plottedData.append(
                self.ax.plot(
                    subplot,
                    linewidth = 1,
                    color     = colors[i],
                )[0]
            )
        
        self.canvas = FigCanvas(self.panel, wx.ID_ANY, self.fig)
        
        self.drawPlot()
            
    
    def drawPlot(self):
        """
        Redraws the plot.
        """
        xmin = self.xmin
        xmax = self.xmax
        ymin = self.ymin
        ymax = self.ymax

        self.ax.set_xbound( lower=xmin, upper=xmax )
        self.ax.set_ybound( lower=ymin, upper=ymax )
        
        # 3. Add ticks to the plot
        if self.xticks:
            self.ax.set_xticks( self.xticks )
        if self.yticks:
            self.ax.set_yticks( self.yticks )
        
        # 4. Add a grid to the chart
        if self.showGrid:
            self.ax.grid( True, color='gray' )
        else:
            self.ax.grid( False )
    
        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly 
        # iterate, and setp already handles this.
        #  
        pylab.setp(self.ax.get_xticklabels(), visible=True)
        
        for i, subplot in enumerate(self.data):
            xdata = []
            ydata = []
            for x, y in subplot:
                xdata.append(x)
                ydata.append(y)
            self.plottedData[i].set_xdata( xdata )
            self.plottedData[i].set_ydata( ydata )
        
        self.canvas.draw()