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


class GraphSAXSWithQRange(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Toolbar, figures
        self.__canvas = CanvasSAXSWithQRange()
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)        
        
    def plot(self, files):
        for f, v in files.items():
            with XPCSResultFile(f) as fd:
                self.__canvas.plot(fd,v)
            
        self.__canvas.draw()
        
    def clear(self):
        self.__canvas.clear()
        

class CanvasSAXSWithQRange(FigureCanvas):
    def __init__(self, parent=None, width=10, height=10, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.__axes = self.__fig.add_subplot(111)
        super().__init__(self.__fig)
        
    def plot(self, file, entries):
        
        q = file.saxs_curve_q
        I = file.saxs_curve_Iq
       
        self.__axes.plot(q, I, label=f"{file.title} {file.filename}")
        
        qmin, qmax = np.inf,0
        
        for e in entries:
            qs   = file.get_q_values(e)
            qmin = min(np.nanmin(qs), qmin)
            qmax = max(np.nanmax(qs), qmax)
        
        (cmapi, normi, mv) = gt.qindex_colors([qmin, qmax])
        
        
        qmap = file.get_2D_parameter('qmap') if 'qmap' in file.available_2D_parameters else file.get_2D_pattern('qmap')
        for e in entries:
            roi_masks = file.get_roi_masks(e)
            
            logger.debug(roi_masks.shape)
            
            q_ranges = np.zeros((roi_masks.shape[0], 4))
            sym = gt.symbol(self._symid)
            self._symid += 1
            labelset = False
            for i in range(roi_masks.shape[0]):
                qM = qmap[roi_masks[i,:,:]]
                
                #print(np.sum(roi_masks[i,:,:]))
                
                if len(qM) == 0:
                    continue
                
                qm = np.mean(qM)
                q_ranges[i,0] = qm
                q_ranges[i,1] = qm - np.min(qM)
                q_ranges[i,2] = np.max(qM) - qm
                q_ranges[i,3] = I[np.argmin(np.abs(q - qm))]
                
                self.__axes.errorbar(q_ranges[i,0],
                                     q_ranges[i,3],
                                     marker=sym,
                                     xerr=q_ranges[i:i+1,1:3].T,
                                     color=cmapi(normi(q_ranges[i,0])),
                                     label=f"{e} {file.filename}" if not labelset else None)
                
                labelset = True
                
        self.__axes.set_xscale('log')
        self.__axes.set_yscale('log')
        self.__axes.set_xlabel('$q (nm^{-1})$')
        self.__axes.set_ylabel('$I(q)$')
        
        self.__axes.legend(fontsize=cmm.default_legend_font_size)
        
    def clear(self):
        self._symid = 0
        self.__axes.cla()

