# -*- coding: utf-8 -*-


import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtWidgets as qtw

import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.markers import MarkerStyle
import matplotlib.cm as cm
import xpcsutilities.tools.graphs as gt

import logging
logger = logging.getLogger(__name__)
        
class ResultFitGraph(qtw.QWidget):
    def __init__(self, results, cmap=None, norm=None):
        super().__init__()
        
        self.__results = results
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Toolbar, figures
        self.__canvas = ResultFitCanvas(cmap, norm)
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)  
        
        # Display options toolbar
        self.__toolbarlayout = qtw.QHBoxLayout()
        self.__layout.addLayout(self.__toolbarlayout)
        
        self.__opt1layout = qtw.QFormLayout()
        self.__toolbarlayout.addLayout(self.__opt1layout)
        
        self.__displayG2_1 = qtw.QCheckBox()
        self.__displayG2_1.setChecked(True)
        self.__opt1layout.addRow("Display rescaled $(g_2-1)/\\beta$", self.__displayG2_1)
        
        self.__displaySep = qtw.QCheckBox()
        self.__displaySep.setChecked(False)
        self.__opt1layout.addRow("Display each functions", self.__displaySep)
        
        self.__btnredraw = qtw.QPushButton("Redraw")
        self.__btnredraw.setMinimumHeight(100)
        self.__toolbarlayout.addWidget(self.__btnredraw)
        self.__btnredraw.clicked.connect(self.plot)
        
        self.plot()
        
    def plot(self):
        self.__canvas.clear()
        self.__canvas.plot(self.__results, self.__displayG2_1.isChecked(), self.__displaySep.isChecked())
        self.__canvas.draw()

class ResultFitCanvas(FigureCanvas):
    def __init__(self, cmap=None, norm=None, parent=None, width=10, height=10, dpi=150):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.__axes = self.__fig.add_subplot(111)
        self.__cmap = cmap
        self.__norm = norm
        self.__cb   = None
        super().__init__(self.__fig)
        
    def plot(self, results, rescale=False, sep=False):
        
        if len(results) > 0 and not 'beta' in results[0]['fitres'] and rescale:
            logger.critical("No contrast (beta) found.")
            qtw.QMessageBox.critical(self, "No contrast", "Can't rescale according to contrast: parameter beta not found")
            rescale = False
            
        for r in results:
            
            cf = r['cf']
            lag = r['lag']
            
            if rescale:
                cf = (cf-1.)/r['fitres']['beta']
                
            plargs = dict()
            
            if self.__cmap is not None and self.__norm is not None:
                plargs['color'] = self.__cmap(self.__norm(r['color']))
                
            self.__axes.plot(lag, cf, 'o', **plargs)
                
            if 'fitfun' in r:
                
                lxm = np.floor(np.log10(min(lag)))
                lxM = np.ceil(np.log10(max(lag)))
                    
                x = np.logspace(lxm, lxM, int(50*(lxM-lxm)))
                
                prms = []
                qs = np.array([r['q'],])
                for i,k in enumerate(r['fitkeys']):
                    prms += [ r['fitres'][k], ]
                    
                funv, funsep, N = r['fitfun'](x,qs,*prms, sepf=True, scale=False)
                
                if 'beta' in r['fitkeys']:
                    if not rescale:
                        funv += 1
                        funsep += 1
                    else:
                        funv = (funv)/r['fitres']['beta']
                        funsep = (funsep)/r['fitres']['beta']                        
                else:
                    if not rescale:
                        funv = (funv)*r['fitres']['beta']+1.
                        funsep = (funsep)*r['fitres']['beta']+1.
                    
                self.__axes.plot(x, funv, **plargs)
                    
                if N>1 and sep :
                    self.__axes.plot(x, funsep, '--', **plargs)
        
        self.__axes.set_xscale('log')
        self.__axes.set_yscale('linear')
        self.__axes.set_xlabel('$lag time (s)$')
        self.__axes.set_ylabel('$(g_2-1)/\\beta$' if rescale else '$g_2$')
        
        if self.__cb is None:
            (cmap, norm) = gt.truncate_colormap(self.__cmap, self.__norm)
            self.__cb = self.__fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap))
        
        #self.__axes.legend(fontsize=7)
        
    def clear(self):
        self.__axes.cla()
        

class ResultParamsFitGraph(qtw.QWidget):
    def __init__(self, results):
        super().__init__()
        
        self.__results = results
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Toolbar, figures
        self.__canvas = ResultParamsFitCanvas(self.__results['params'].keys())
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)  
        
        # Display options toolbar
        self.__toolbarlayout = qtw.QHBoxLayout()
        self.__layout.addLayout(self.__toolbarlayout)
        
        # OPT1: log axes
        self.__opt1layout = qtw.QFormLayout()
        self.__toolbarlayout.addLayout(self.__opt1layout)
        
        self.__opt_logx = qtw.QCheckBox()
        self.__opt1layout.addRow('Log x', self.__opt_logx)
        
        self.__opt_logy = dict()
        for k in self.__results['params']:
            cb = qtw.QCheckBox()
            self.__opt1layout.addRow('Log %s'%k, cb)
            self.__opt_logy[k] = cb
            
        # opt2: color, marker, xaxis selection
        self.__opt2layout = qtw.QFormLayout()
        self.__toolbarlayout.addLayout(self.__opt2layout)
        
        self.__opt_x_axis = qtw.QComboBox()
        self.__opt_x_axis.addItem('q', ResultParamsFitCanvas.OPT_Q)
        self.__opt_x_axis.addItem('time', ResultParamsFitCanvas.OPT_TIME)
        self.__opt2layout.addRow("x axis", self.__opt_x_axis)
        
        self.__opt_c_axis = qtw.QComboBox()
        self.__opt_c_axis.addItem('None', ResultParamsFitCanvas.OPT_NONE)
        self.__opt_c_axis.addItem('q', ResultParamsFitCanvas.OPT_Q)
        self.__opt_c_axis.addItem('time', ResultParamsFitCanvas.OPT_TIME)
        self.__opt_c_axis.addItem('direction', ResultParamsFitCanvas.OPT_DIR)
        self.__opt_c_axis.setCurrentIndex(2)
        self.__opt2layout.addRow("color axis", self.__opt_c_axis)
        
        self.__opt_m_axis = qtw.QComboBox()
        self.__opt_m_axis.addItem('Direction + file', ResultParamsFitCanvas.OPT_DIRFILE)
        self.__opt_m_axis.addItem('Direction', ResultParamsFitCanvas.OPT_DIR)
        self.__opt_m_axis.addItem('File', ResultParamsFitCanvas.OPT_FILE)
        self.__opt2layout.addRow("Marker", self.__opt_m_axis)
            
        # Redraw button
        self.__btnredraw = qtw.QPushButton("Redraw")
        self.__btnredraw.setMinimumHeight(100)
        self.__toolbarlayout.addWidget(self.__btnredraw)
        self.__btnredraw.clicked.connect(self.plot)
        
        
        files = []
        dirs = []
        mids = []
        
        self.__results['fid'] = []
        self.__results['did'] = []
        self.__results['mid'] = []
        
        for i in range(len(self.__results['q'])):
            if self.__results['file'][i] not in files:
                files += [self.__results['file'][i], ]
                
            if self.__results['dir'][i] not in files:
                dirs += [self.__results['dir'][i], ]
                
            fid = files.index(self.__results['file'][i])
            did = dirs.index(self.__results['dir'][i])
            
            mark = '%i_%i'%(fid, did)
            
            if mark not in mids:
                mids += [mark, ]
                
            mid = mids.index(mark)
            
            self.__results['fid'] += [fid, ]
            self.__results['did'] += [did, ]
            self.__results['mid'] += [mid, ]
            
        self.__results['q'] = np.array(self.__results['q'])
        self.__results['tsr'] = np.array(self.__results['tsr'])
        self.__results['fid'] = np.array(self.__results['fid'])
        self.__results['did'] = np.array(self.__results['did'])
        self.__results['mid'] = np.array(self.__results['mid'])
        
        for k in self.__results['params']:
            self.__results['params'][k] = np.array(self.__results['params'][k])
        
        self.plot()
        
    def plot(self):        
        self.__canvas.clear()
        self.__canvas.plot(self.__results,
                           logx=self.__opt_logx.isChecked(),
                           logy={ k:cb.isChecked() for k,cb in self.__opt_logy.items() },
                           xaxis = self.__opt_x_axis.currentData(),
                           caxis = self.__opt_c_axis.currentData(),
                           mark = self.__opt_m_axis.currentData()
                           )
        self.__canvas.draw()

class ResultParamsFitCanvas(FigureCanvas):
    
    OPT_NONE    = 0
    OPT_Q       = 1
    OPT_TIME    = 2
    OPT_DIR     = 3
    OPT_FILE    = 4
    OPT_DIRFILE = 5
    
    def __init__(self, params, parent=None, width=10, height=10, dpi=150):
        self.__params = params
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        
        N = len(params)
        nc = int(np.ceil(N**.5))
        nr = int(nc - np.floor((nc**2-N)/nc))
        
        ax = self.__fig.subplots(nr,nc,sharex='col', squeeze=False)
        self.__axes = [ a for sub in ax for a in sub ]
        
        super().__init__(self.__fig)
        
    def plot(self, results, logx, logy, xaxis, caxis, mark):
        
        if xaxis == self.OPT_Q:
            x = results['q']
        elif xaxis == self.OPT_TIME:
            x = results['tsr']
        else:
            raise ValueError('Unsuported x axis, %s'%xaxis)
            
        if caxis == self.OPT_Q:
            c = results['q']
        elif caxis == self.OPT_TIME:
            c = results['tsr']
        elif caxis == self.OPT_DIR:
            c = results['did']
        elif caxis == self.OPT_NONE:
            c = None
            cmap, norm = None, None
        else:
            raise ValueError('Unsuported c axis %s'%caxis)
            
        if c is not None:
            cmap, norm, M = gt.qindex_colors(c)
            cmap, norm = gt.truncate_colormap(cmap, norm)
            
        if mark == self.OPT_DIR:
            m = results['did']
        elif mark == self.OPT_FILE:
            m = results['fid']
        elif mark == self.OPT_DIRFILE:
            m = results['mid']
        else:
            raise ValueError('Unsuported m axis %s'%mark)
        
        markers = ('o','s','v','P','^','*','<','D','>','X','p')
        
        for j,M in enumerate(np.unique(m)):
            msk = m == M
            marker_id = np.mod(j, len(markers))
            
            for i,k in enumerate(self.__params):
                self.__axes[i].scatter(x[msk],
                           results['params'][k][msk],
                           c=c[msk] if c is not None else None,
                           cmap=cmap, norm=norm,
                           marker=MarkerStyle(markers[marker_id]))

        for i,k in enumerate(self.__params):
            if logx:
                self.__axes[i].set_xscale('log')
            
            if logy[k]:
                self.__axes[i].set_yscale('log')
            
            self.__axes[i].set_title(k)
            self.__axes[i].grid()
        
    def clear(self):
        for a in self.__axes:
            a.cla()
        