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
from constants import *

class LineChart:
    
    def __init__(self, parent, data, title, xlabel, ylabel, xmin=None, xmax=None, ymin=None, ymax=None, xticks=None, yticks=None, xticks_minor=None, yticks_minor=None, labels=None, showGrid=False):
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
        self.labels       = labels
        self.showGrid     = showGrid
        
        self.plottedData = []
        
        
        self.createChart()
        

    def createChart(self):
        """
        Creates the chart.
        """
        self.dpi    = 100
        width  = self.panel.GetSize()[0] * 0.01041666666667 # covert pixels to inches
        height = self.panel.GetSize()[1] * 0.01041666666667
        margin = 0.4
        fontsize=8
        
        # Create the figure and devide the space into two axes (one invisible for the legend)
        self.fig = plt.figure( figsize=(width, height-margin), dpi=self.dpi )
        self.ax  = plt.subplot2grid((1, 6), (0, 0), colspan=5)
        self.cax = plt.subplot2grid((1, 6), (0, 5), colspan=1, visible=False)
        
        self.ax.set_title(  self.title,  size=12)
        self.ax.set_xlabel( self.xlabel, size=fontsize)
        self.ax.set_ylabel( self.ylabel, size=fontsize)
        self.ax.set_axis_bgcolor('white')

#        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        colors = ['red', 'gray', 'yellow', 'green']
        # Plot the data and save the reference
        for i, subplot in enumerate(self.data):
            self.plottedData.append(
                self.ax.plot(
                    subplot,
                    label     = self.labels[i],
                    linewidth = 1,
                    color     = colors[i],
                )[0]
            )
        
        self.ax.set_xbound( lower=self.xmin, upper=self.xmax )
        self.ax.set_ybound( lower=self.ymin, upper=self.ymax )
        
        # 3. Add ticks to the plot
        if self.xticks:
            self.ax.set_xticks( self.xticks )
        if self.yticks:
            self.ax.set_yticks( self.yticks )
        self.ax.tick_params(axis='both', which='major', labelsize=fontsize) # set the font size of the ticks
        
        # 4. Add a grid to the chart
        if self.showGrid:
            self.ax.grid( True, color='gray' )
        else:
            self.ax.grid( False )
        
        # 5. Add a legend
        lgd = self.ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), prop={'size': fontsize})
        lgd.get_frame().set_alpha(0.3)
        
        self.canvas = FigCanvas(self.panel, wx.ID_ANY, self.fig)
        
        self.drawPlot()
            
    
    def drawPlot(self):
        """
        Extract and draw the data for every subplot.
        """
        for i, subplot in enumerate(self.data):
            xdata = []
            ydata = []
            for x, y in subplot:
                xdata.append(x)
                ydata.append(y)
            self.plottedData[i].set_xdata( xdata )
            self.plottedData[i].set_ydata( ydata )
        
        self.canvas.draw()



class HeatMap:
    
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
        
        
        self.createChart()
        

    def createChart(self):
        """
        Creates the chart.
        """
        self.dpi    = 100
        width  = self.panel.GetSize()[0] * 0.01041666666667 # covert pixels to inches
        height = self.panel.GetSize()[1] * 0.01041666666667
        margin = 0.4
        fontsize=8
        
        # Create the figure and devide the space into two axes (one invisible for the legend)
        self.fig = plt.figure( figsize=(width, height-margin), dpi=self.dpi )
        self.ax  = plt.subplot2grid((1, 6), (0, 0), colspan=5)
        self.cax = plt.subplot2grid((1, 6), (0, 5), colspan=1, visible=False)
        
        self.ax.set_title(  self.title,  size=12)
        self.ax.set_xlabel( self.xlabel, size=fontsize)
        self.ax.set_ylabel( self.ylabel, size=fontsize)
        self.ax.set_axis_bgcolor('white')
        
        xdata = DAYS
        ydata = LATS
        zdata = np.zeros((ydata.shape[0], xdata.shape[0]-1))
        xdata, ydata = np.meshgrid(xdata, ydata)
        zmin = 0
        zmax = 550
        self.plottedData = self.ax.pcolormesh(xdata, ydata, zdata, cmap='terrain', vmin=zmin, vmax=zmax)
        
        self.ax.set_xbound( lower=self.xmin, upper=self.xmax )
        self.ax.set_ybound( lower=self.ymin, upper=self.ymax )
        
        # 3. Add ticks to the plot
        if self.xticks:
            self.ax.set_xticks( self.xticks )
        if self.yticks:
            self.ax.set_yticks( self.yticks )
        self.ax.tick_params(axis='both', which='major', labelsize=fontsize) # set the font size of the ticks
        
        # 4. Add a grid to the chart
        if self.showGrid:
            self.ax.grid( True, color='gray' )
        else:
            self.ax.grid( False )
        
        # 5. Add colorbar
        cbar = plt.colorbar( self.plottedData, ticks=range(zmin, zmax, 100) )
        cbar.ax.set_title( u"W/m²", fontsize=fontsize)
        cbar.ax.tick_params(labelsize=fontsize)
        
        self.canvas = FigCanvas(self.panel, wx.ID_ANY, self.fig)

        self.drawPlot()
            
    
    def drawPlot(self):
        """
        Extract and draw the data for every subplot.
        """
        zdata = np.array(self.data)
        self.plottedData.set_array( zdata.ravel() )            
        
        self.canvas.draw()