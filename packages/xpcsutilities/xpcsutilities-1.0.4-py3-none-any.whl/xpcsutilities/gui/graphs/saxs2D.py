# -*- coding: utf-8 -*-

import matplotlib
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


class GraphSAXSPattern(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Figure
        self.__canvas = CanvasSAXSPattern()
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)
        
        # Checkbox to display mask and qmask
        self.__optlayout = qtw.QHBoxLayout()
        self.__opt1layout = qtw.QFormLayout()
        self.__layout.addLayout(self.__optlayout)
        self.__optlayout.addLayout(self.__opt1layout)
        
        self.__checkShowMask = qtw.QCheckBox(self)
        self.__checkShowMask.setChecked(True)
        self.__opt1layout.addRow("Display mask", self.__checkShowMask)
        
        self.__checkShowQMask= qtw.QCheckBox(self)
        self.__checkShowQMask.setChecked(True)
        self.__opt1layout.addRow("Display qmask", self.__checkShowQMask)
        
        self.__plotSelector = qtw.QComboBox(self)
        
        self.__opt1layout.addRow("Plot", self.__plotSelector)
        
    
    def clear(self):
        self.__canvas.clear()
        
    def plot(self, files):
        
        N = 0
        for k,v in files.items():
            N += len(v)
        
        self.__canvas.setNPlots(N)
        
        i = 0
        for k,v in files.items():
            with XPCSResultFile(k) as fd:
                if i == 0:
                    _prev = self.__plotSelector.currentText()
                    self.__plotSelector.clear()
                    self.__plotSelector.addItems(fd.available_2D_patterns + fd.available_2D_parameters)
                    
                    logger.debug(_prev)
                    self.__plotSelector.setCurrentText(fd.default_2D_pattern if _prev == "" else _prev)
                    
                for d in v:
                    self.__canvas.plot(fd,i,d, self.__plotSelector.currentText(), self.__checkShowQMask.isChecked(), self.__checkShowMask.isChecked())
                    i += 1
            
        self.__canvas.draw()
        
        
class CanvasSAXSPattern(FigureCanvas):
    
    PLOT_CORRECTED  = 0
    PLOT_RAW        = 1
    PLOT_GAUSS      = 2
    PLOT_SATURATION = 3
    
    def __init__(self, parent=None, width=5, height=5, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(self.__fig)
        
        self.setMaximumHeight(100000)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        
    def clear(self):
        self.__fig.clf()
        
    def _format_coord(self, x, y):
        
        xi = int(x)
        yi = int(y)
        
        R = f"x, y = ({xi}, {yi})"
        
        if xi >= 0 and xi < self._qmap.shape[1] and yi >=0 and yi < self._qmap.shape[0]:
            if self._tmap is not None:
                R += f" q; theta = ({self._qmap[yi,xi]:.01e}; {self._tmap[yi,xi]:.02f})"
            else:
                R += f" q = {self._qmap[yi, xi]:.01e}"
            
        return R
        
    
    def _get_cursor_data(self, event):
        
        xi, yi = int(event.xdata), int(event.ydata)
        
        value = self._values[yi, xi]
        rois  = np.where(self._roi_masks[:, yi, xi])[0]
        mask  = ~np.isnan(self._mask[yi, xi])
        
        masks = ""
        if mask:
            masks = "[ masked ]"
        elif len(rois) > 0:
            masks = ", ".join([f"{v:d}" for v in rois])
            masks = f"q_index = [ {masks} ]"
        return f"I={value:.03e} {masks}"
        
        
    def setNPlots(self, N):
        
        nCols = int(np.max([N**.5//1.22,1]))
        nRows = int(np.max([np.ceil(N/nCols),1]))
        
        gs = self.__fig.add_gridspec(nRows, nCols*2,width_ratios=[*[30, 1]*nCols])
        
        self.__axes = []
        
        for y in range(nRows):
            for x in range(nCols):
                self.__axes += [(self.__fig.add_subplot(gs[y,x*2]), self.__fig.add_subplot(gs[y,x*2+1])), ]
        
    def plot(self, file, ii, dirk, plot_sel, draw_q=True, draw_mask=True):
        
        ax = self.__axes[ii][0]
        ax.set_title(f"{file.title} {file.filename} {dirk}", fontsize=cmm.default_title_font_size)
        
        if dirk not in file.analysis_keys:
            return
        
        patt = None
        
        if plot_sel in file.available_2D_patterns:
            patt = file.get_2D_pattern(plot_sel)
        elif plot_sel in file.available_2D_parameters:
            patt = file.get_2D_parameter(plot_sel)
            
        if patt is None:
            logger.warning("Not available.")
            return
    
        cmap = mpl.cm.jet
        norm = mpl.colors.LogNorm()
        
        # qmask colorbar
        roi_masks = file.get_roi_masks(dirk)
        (cmapi, normi, mv) = gt.qindex_colors([0, roi_masks.shape[0]-1])
        
        cmapi.set_bad(alpha=0)
        
        ax.imshow(patt, cmap=cmap, norm=norm, interpolation='none')
        
        
        mmask = np.ones_like(patt, dtype=np.float32)
        mmask[file.get_2D_parameter('mask') == 1] = np.nan
        
        if draw_mask:
            normm = mpl.colors.Normalize(vmin=0, vmax=1)
            ax.imshow(mmask, cmap='gray', norm=normm, alpha=.6)
            
        roiN = np.zeros(roi_masks.shape[1:], dtype=np.float32)
        roiS = np.zeros(roi_masks.shape[1:], dtype=np.float32)
        if draw_q:
            for i in range(roi_masks.shape[0]):
                roiN[roi_masks[i]] += 1
                roiS[roi_masks[i]] += i
                
            ax.imshow(roiS/roiN, cmap=cmapi, norm=normi, alpha=1.-(0.6)**roiN)
            
        self._values = patt
        self._roi_masks = roi_masks
        self._mask = mmask
        self._qmap = file.get_2D_parameter('qmap') if 'qmap' in file.available_2D_parameters else file.get_2D_pattern('qmap')
        self._tmap = file.get_2D_parameter('thetamap') if 'thetamap' in file.available_2D_parameters else None 
        
        ax1 = self.__axes[ii][1]
        #ax2 = self.__axes[ii][2]
        
        self.__fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax1, label=None)
        #self.__fig.colorbar(mpl.cm.ScalarMappable(norm=normi, cmap=cmapi), cax=ax2, label="q", format=mpl.ticker.FuncFormatter(lambda x,p: "%.3e"%(file.qs[np.where(x == q_ranges[:,0])])), ticks=file.q_ranges[::((file.q_ranges.shape[0]//8)+1),0])


        ax.format_coord = self._format_coord
        ax.format_cursor_data = lambda s: s
        ax.get_cursor_data = self._get_cursor_data
        ax.mouseover = True
        logger.debug(ax.mouseover)
        
#        while 'motion_notify_event' in self.callbacks.callbacks:
#            self.callbacks.callbacks.pop('motion_notify_event')
#            
#        self.mpl_connect('motion_notify_event', self.onHover)
