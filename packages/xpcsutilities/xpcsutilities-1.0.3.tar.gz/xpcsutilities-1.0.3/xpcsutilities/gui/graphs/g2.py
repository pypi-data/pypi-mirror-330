# -*- coding: utf-8 -*-

import matplotlib
import os
matplotlib.use('Qt5Agg')

import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

import xpcsutilities.tools.graphs as gt
from xpcsutilities.tools.result_file import XPCSResultFile
import numpy as np
import scipy.optimize as opt

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import xpcsutilities.tools.common as cmm

import logging
logger = logging.getLogger(__name__)


       
class GraphCorrelation(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Figure
        self.__canvas = CanvasCorrelation()
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)
        
        # Checkbox to merge files and directions on same plot
        self.__optlayout = qtw.QHBoxLayout()
        self.__layout.addLayout(self.__optlayout)
        
        # Plot setup group
        self.__opt1group = qtw.QGroupBox("Plot setup")
        self.__optlayout.addWidget(self.__opt1group
                                   )
        self.__opt1layout = qtw.QFormLayout()
        self.__opt1group.setLayout(self.__opt1layout)
        
        self.__checkLogX = qtw.QCheckBox(self)
        self.__checkLogX.setChecked(True)
        self.__opt1layout.addRow("Log x-scale", self.__checkLogX)
        
        self.__checkLogY = qtw.QCheckBox(self)
        self.__checkLogY.setChecked(False)
        self.__opt1layout.addRow("Log y-scale", self.__checkLogY)
        
        self.__checkG2_1 = qtw.QCheckBox(self)
        self.__checkG2_1.setChecked(False)
        self.__opt1layout.addRow("g_2-1", self.__checkG2_1)
        
        self.__checkGrid = qtw.QCheckBox(self)
        self.__checkGrid.setChecked(False)
        self.__opt1layout.addRow("Grid", self.__checkGrid)
        
        self.__checkLegend = qtw.QCheckBox(self)
        self.__checkLegend.setChecked(True)
        self.__opt1layout.addRow("Legend", self.__checkLegend)
        
        self.__colorbarscale = qtw.QComboBox()
        self.__colorbarscale.addItems(["default", 'ocean', 'gist_earth', 'terrain',
                      'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                      'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                      'turbo', 'nipy_spectral', 'gist_ncar', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv'])
        self.__opt1layout.addRow("q colormap: ", self.__colorbarscale)
        
        # Sparcification
        
        self.__opt4group = qtw.QGroupBox("Curve selection")
        self.__optlayout.addWidget(self.__opt4group)
        
        self.__opt4layout = qtw.QFormLayout()
        self.__opt4group.setLayout(self.__opt4layout)
        
        self.__curvesparse = qtw.QSpinBox()
        self.__curvesparse.setSuffix(" curves")
        self.__curvesparse.setMinimum(1)
        self.__curvesparse.setMaximum(20)
        self.__opt4layout.addRow("Display each ", self.__curvesparse)
        
        self.__curvesoff = qtw.QSpinBox()
        self.__curvesoff.setSuffix(" curves")
        self.__curvesoff.setMinimum(0)
        self.__curvesoff.setMaximum(20)
        self.__opt4layout.addRow("Offset ", self.__curvesoff)
        
        # self.__xsparsemode = qtw.QComboBox()
        # self.__xsparsemode.addItems(["Off", "Number of points (lin)", "Number of points (log)", "Points per decade (log)"])
        # self.__opt4layout.addRow("Lag time sparcification: ", self.__xsparsemode)
        
        # self.__xsparse = qtw.QSpinBox()
        # self.__xsparse.setSuffix("pt/dec or pt")
        # self.__xsparse.setMinimum(1)
        # self.__xsparse.setMaximum(20)
        # self.__opt4layout.addRow("Sparcification factor ", self.__xsparse)
        
        # q colorbar
        
        self.__opt2group = qtw.QGroupBox("Manual q colorbar")
        self.__optlayout.addWidget(self.__opt2group)
        
        self.__opt2group.setCheckable(True)
        self.__opt2group.setChecked(False)
        self.__opt2layout = qtw.QFormLayout()
        self.__opt2group.setLayout(self.__opt2layout)
        
        self.__minqcolorbar = qtw.QDoubleSpinBox()
        self.__opt2layout.addRow("Minimum q:", self.__minqcolorbar)
        self.__minqcolorbar.setSuffix(" nm-1")
        self.__minqcolorbar.setMinimum(0)
        self.__minqcolorbar.setMaximum(100)
        self.__minqcolorbar.setDecimals(4)
        self.__minqcolorbar.setSingleStep(.005)
        self.__minqcolorbar.setValue(0.003)
        
        self.__maxqcolorbar = qtw.QDoubleSpinBox()
        self.__opt2layout.addRow("Maximum q:", self.__maxqcolorbar)
        self.__maxqcolorbar.setSuffix(" nm-1")
        self.__maxqcolorbar.setMinimum(0)
        self.__maxqcolorbar.setMaximum(100)
        self.__maxqcolorbar.setDecimals(4)
        self.__maxqcolorbar.setSingleStep(.005)
        self.__maxqcolorbar.setValue(0.01)
        
        # q restrict
        
        self.__opt3group = qtw.QGroupBox("Restrict q range")
        self.__optlayout.addWidget(self.__opt3group)
        
        self.__opt3group.setCheckable(True)
        self.__opt3group.setChecked(False)
        self.__opt3layout = qtw.QFormLayout()
        self.__opt3group.setLayout(self.__opt3layout)
        
        self.__minq = qtw.QDoubleSpinBox()
        self.__opt3layout.addRow("Minimum q:", self.__minq)
        self.__minq.setSuffix(" nm-1")
        self.__minq.setMinimum(0)
        self.__minq.setMaximum(100)
        self.__minq.setDecimals(4)
        self.__minq.setSingleStep(.005)
        self.__minq.setValue(0.003)
        
        self.__maxq = qtw.QDoubleSpinBox()
        self.__opt3layout.addRow("Maximum q:", self.__maxq)
        self.__maxq.setSuffix(" nm-1")
        self.__maxq.setMinimum(0)
        self.__maxq.setMaximum(100)
        self.__maxq.setDecimals(4)
        self.__maxq.setSingleStep(.005)
        self.__maxq.setValue(0.01)
        
    def clear(self):
        self.__canvas.clear()
        
    def plot(self, filelist):
        
        if not self.__opt2group.isChecked() or not self.__opt3group.isChecked() :
            minq = None
            maxq = None
            for f, d in filelist.items():
                with XPCSResultFile(f) as fd:
                    
                    qs = fd.get_q_values(d[0])
                    print(qs)
                    
                    if minq is None or np.nanmin(qs) < minq:
                        minq = np.nanmin(qs)-.001
                    if maxq is None or np.nanmax(qs) > maxq:
                        maxq = np.nanmax(qs)+.001
                        
        
                        
            if not self.__opt3group.isChecked():
                self.__minq.setValue(minq)
                self.__maxq.setValue(maxq)
        
            if not self.__opt2group.isChecked():
                self.__minqcolorbar.setValue(self.__minq.value())
                self.__maxqcolorbar.setValue(self.__maxq.value())
                
        self.__canvas.setupColormap(self.__colorbarscale.currentText(), self.__minqcolorbar.value(), self.__maxqcolorbar.value())
        
        fid = 0
        off = self.__curvesoff.value()
        each= self.__curvesparse.value()
        
        for f,v in filelist.items():
            logger.debug((f,v))
            with XPCSResultFile(f) as fd:
                for j,k in enumerate(v):
                    logger.debug((f,k))
                    
                    (ts, cf, std) = fd.get_correlations(k)
                    
                    logger.debug(ts)
                    
                    qs = fd.get_q_values(k)
                    
                    if std is None:
                        std =cf*0
                        
                    if self.__checkG2_1.isChecked():
                        cf -= 1
                        
                    msk = np.logical_and(qs >= self.__minq.value(), qs <= self.__maxq.value())
                    logger.debug((qs, msk))
                    qs  =  qs[msk]
                    cf  =  cf[msk,:]
                    std = std[msk,:]
                    
                    fnam = os.path.basename(f)
                    
                    self.__canvas.plot(ts, cf[off::each,:], std[off::each,:], qs[off::each],
                                       f"{fd.title} {fnam} {k}",
                                       fid, j)
                fid += 1
            
        self.__canvas.setupAxes(self.__checkLogX.isChecked(),
                                self.__checkLogY.isChecked(),
                                self.__checkGrid.isChecked(),
                                self.__checkLegend.isChecked(),                                
                                self.__checkG2_1.isChecked())
        self.__canvas.draw()
        
        
class CanvasCorrelation(FigureCanvas):
    def __init__(self, parent=None, width=5, height=5, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(self.__fig)
        
        self.setMaximumHeight(100000)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        
        gs = self.__fig.add_gridspec(1, 2, width_ratios=[35, 1])
        self.__ax  = self.__fig.add_subplot(gs[0,0]) 
        self.__cax = self.__fig.add_subplot(gs[0,1]) 
        
    def clear(self):
        self.__ax.cla()
        self.__cax.cla()    
        
    def setupColormap(self, colormap, minq, maxq):
        
        self.__cmap, self.__norm, mv = gt.qindex_colors([minq, maxq], colormap=colormap)
        self.__fig.colorbar(mpl.cm.ScalarMappable(norm=self.__norm, cmap=self.__cmap), cax=self.__cax, label='$q (nm^{-1})$')
        
    def setupAxes(self, logx, logy, grid, legend, g2_1):
        
        if logx:
            self.__ax.set_xscale('log')
        else:
            self.__ax.set_xscale('linear')
        
        if logy:
            self.__ax.set_yscale('log')
        else:
            self.__ax.set_yscale('linear')
            
        self.__ax.grid(grid)
        
        if legend:
            self.__ax.legend(fontsize=cmm.default_legend_font_size)
        
        self.__ax.set_xlabel(r'Lag time $\tau~(s)$')
        self.__ax.set_ylabel(r'$g_2(q,t) - 1$' if g2_1 else r'$g_2(q,t)$')
                
    def symbols(self, x, y):
        symbols = 'o^sXvD>*<P'
        fill = ['full','none','left','right','top','bottom']
        
        sid = np.mod(y, len(symbols))
        fid = np.mod(x, len(fill))
        
        return {'marker': symbols[sid], 'fillstyle': fill[fid], 'markersize': 4}
                
        
    def plot(self, ts, cf, std, qs, legend, fid=0, cid=0):
        
        mark = self.symbols(cid, fid)

        for i, q in enumerate(qs):
            logger.debug((ts.shape, cf[:,i].shape, std[:,i].shape))
            #self.__ax.errorbar(ts, cf[:,i], std[:,i], **mark, color=self.__cmap(self.__norm(q)), label=legend if i == 0 else None )
            self.__ax.plot(ts, cf[i,:], **mark, color=self.__cmap(self.__norm(q)), label=legend if i == 0 else None )


