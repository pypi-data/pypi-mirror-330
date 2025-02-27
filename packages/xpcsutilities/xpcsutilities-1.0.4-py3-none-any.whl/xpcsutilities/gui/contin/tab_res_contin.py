# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as qtw

import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import xpcsutilities.tools.graphs as gt
import xpcsutilities.tools.common as cmm
import xpcsutilities.tools.contin as contin

class ContinResult(qtw.QWidget):
    """
    Display the result of CONTIN analysis
    """
    
    def __init__(self):
        """
        Initialize the view with graph
        """
        
        super().__init__()
        
        self.__layout = qtw.QGridLayout()
        self.setLayout(self.__layout)
        
        self.__Gcanvas = Contin2DCanvas()
        self.__navG = NavigationToolbar(self.__Gcanvas, self)
        
        self.__layout.addWidget(self.__navG, 0,0)
        self.__layout.addWidget(self.__Gcanvas, 1,0)
        
        self.__g2canvas = Contin1DCanvas()        
        self.__navg2 = NavigationToolbar(self.__g2canvas, self)
        self.__layout.addWidget(self.__navg2, 0,1)        
        self.__layout.addWidget(self.__g2canvas, 1,1)
        
        self.__residuecanvas = Contin1DCanvas()  
        self.__navres = NavigationToolbar(self.__residuecanvas, self)
        self.__layout.addWidget(self.__navres, 2,1)           
        self.__layout.addWidget(self.__residuecanvas, 3,1)
        
        
    def plot(self, q, tau, cf, s, beta, G):
        """
        Display!
        """
        
        self.__Gcanvas.plot(q, s, G*s[:,None])
        
        cfmod = np.zeros_like(cf)
        for i, qv in enumerate(q):
            cfmod[:,i] = contin.g2LT(s, G[:,i], tau, beta[i])
            
        self.__g2canvas.plot(tau, cf-1, q, 'o')
        self.__g2canvas.plot(tau, cfmod, q, '-')
        
        self.__residuecanvas.plot(tau, cfmod-(cf-1), q)
        
        

class Contin1DCanvas(FigureCanvas):
    """
    Display 1d curves with curves colorized with q
    """
    
    def __init__(self, parent=None, width=5, height=5, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(self.__fig)
        
        gs = self.__fig.add_gridspec(1, 2, width_ratios=[35, 1])
        self.__ax  = self.__fig.add_subplot(gs[0,0]) 
        self.__cax = self.__fig.add_subplot(gs[0,1]) 
        
    def plot(self, x, y, c, *opts, **kopts):
        """
        Plot y(x, c)
        """
        
        cmap = mpl.cm.jet
        norm = mpl.colors.LogNorm(vmin=np.min(c), vmax=np.max(c))
        
        for i, cv in enumerate(c):
            self.__ax.plot(x, y[:,i], *opts, color=cmap(norm(cv)), **kopts)
            
            
        self.__ax.set_xscale('log')
        self.__ax.set_xlabel('$\tau (s)$')
        self.__ax.set_ylabel('$g_2-1$')
        self.__fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=self.__cax, label='$q (nm^{-1})$')
        
        
class Contin2DCanvas(FigureCanvas):
    """
    Display 2d contin map
    """
    
    def __init__(self, parent=None, width=5, height=5, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(self.__fig)
        
        gs = self.__fig.add_gridspec(1, 2, width_ratios=[35, 1])
        self.__ax  = self.__fig.add_subplot(gs[0,0]) 
        self.__cax = self.__fig.add_subplot(gs[0,1]) 
        
    def plot(self, x, y, z, **kopts):
        """
        Plot z(x, y)
        """
        
        cmap = mpl.cm.jet
        norm = mpl.colors.Normalize(vmin=np.min(z), vmax=np.max(z))
        
        self.__ax.pcolormesh(x, y, z, cmap=cmap, norm=norm, **kopts)
        self.__ax.set_xscale('log')
        self.__ax.set_yscale('log')
        
        self.__ax.set_xlabel('$q (nm^{-1})$')
        self.__ax.set_ylabel('$s (s)$')
            
        self.__fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=self.__cax, label='$G*s$')


