

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
        
                 
class Graph2tCorrelation(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        #Layout
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        #Figure
        self.__canvas = Canvas2tCorrelation()
        self.__nav = NavigationToolbar(self.__canvas, self)
        
        # Add to layout
        self.__layout.addWidget(self.__nav)
        self.__layout.addWidget(self.__canvas)
        
        self.__optlayout = qtw.QHBoxLayout()
        self.__layout.addLayout(self.__optlayout)
        
        # Data selection  
        self.__grp0 = qtw.QGroupBox("Data selection")
        self.__optlayout.addWidget(self.__grp0)
        
        self.__grp0l= qtw.QFormLayout()
        self.__grp0.setLayout(self.__grp0l)
        
        # Index selection checkboxes
        self.__optindexlayout = qtw.QFormLayout()
        self.__optlayout.addLayout(self.__optindexlayout)
        self.__indexescombo = qtw.QComboBox()
        self.__grp0l.addRow("q-index:", self.__indexescombo)
        
        # Plot selection
        self.__grp1 = qtw.QGroupBox("Plot settings")
        self.__optlayout.addWidget(self.__grp1)
        
        self.__grp1l= qtw.QFormLayout()
        self.__grp1.setLayout(self.__grp1l)
        
        self.__plottype = qtw.QComboBox()
        self.__plottype.insertItem(Canvas2tCorrelation.PLOT_TS_AGE_LOG, 'lag time(log); age(lin)')
        self.__plottype.insertItem(Canvas2tCorrelation.PLOT_TS_AGE_LIN, 'lag time(lin); age(lin)')
        self.__plottype.insertItem(Canvas2tCorrelation.PLOT_XY, 'Frame(lin); Frame(lin)')
        self.__grp1l.addRow("Plot type", self.__plottype)
        
        
        self.__lagsparcification = qtw.QComboBox()
        self.__lagsparcification.addItem('None', Canvas2tCorrelation.NO_SPARCIFICATION)
        self.__lagsparcification.addItem('Lin', Canvas2tCorrelation.LIN_SPARCIFICATION)
        self.__lagsparcification.addItem('Log', Canvas2tCorrelation.LOG_SPARCIFICATION)
        self.__grp1l.addRow("Lag time resamping", self.__lagsparcification)
        
        self.__Nlagresample = qtw.QSpinBox()
        self.__Nlagresample.setMinimum(1)
        self.__Nlagresample.setMaximum(100000)
        self.__Nlagresample.setValue(256)
        self.__grp1l.addRow('Number of lag points', self.__Nlagresample)
        
        self.__agesparcification = qtw.QComboBox()
        self.__agesparcification.addItem('None', Canvas2tCorrelation.NO_SPARCIFICATION)
        self.__agesparcification.addItem('Lin', Canvas2tCorrelation.LIN_SPARCIFICATION)
        self.__agesparcification.addItem('Log', Canvas2tCorrelation.LOG_SPARCIFICATION)
        self.__grp1l.addRow("Age resamping", self.__agesparcification)
        
        self.__Nageresample = qtw.QSpinBox()
        self.__Nageresample.setMinimum(1)
        self.__Nageresample.setMaximum(100000)
        self.__Nageresample.setValue(1000)   
        self.__grp1l.addRow('Number of age points', self.__Nageresample)     
        
        self.__opt2group = qtw.QGroupBox("Colorbar")
        self.__optlayout.addWidget(self.__opt2group)
        
        # self.__opt2group.setCheckable(True)
        # self.__opt2group.setChecked(False)
        self.__opt2layout = qtw.QFormLayout()
        self.__opt2group.setLayout(self.__opt2layout)
        
        self.__mincolorbar = qtw.QDoubleSpinBox()
        self.__opt2layout.addRow("Minimum:", self.__mincolorbar)
        self.__mincolorbar.setMinimum(0)
        self.__mincolorbar.setMaximum(100)
        self.__mincolorbar.setDecimals(4)
        self.__mincolorbar.setSingleStep(.01)
        self.__mincolorbar.setValue(.8)
        
        self.__maxcolorbar = qtw.QDoubleSpinBox()
        self.__opt2layout.addRow("Maximum:", self.__maxcolorbar)
        self.__maxcolorbar.setMinimum(0)
        self.__maxcolorbar.setMaximum(100)
        self.__maxcolorbar.setDecimals(4)
        self.__maxcolorbar.setSingleStep(.01)
        self.__maxcolorbar.setValue(1.5)
        
        self.__colorbarscale = qtw.QComboBox()
        self.__colorbarscale.addItems(['jet', 'ocean', 'gist_earth', 'terrain',
                      'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                      'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                      'turbo', 'nipy_spectral', 'gist_ncar', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                      'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                      'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                      'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                      'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
                      'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv'])
        self.__opt2layout.addRow("Colormap: ", self.__colorbarscale)

        
    def plot(self, files):
        indexes = np.empty((0,),dtype=np.int16)
        cindex = self.__indexescombo.currentIndex()
        
        N = 0
        for f,d in files.items():
            print(f, d)
            with XPCSResultFile(f) as fd:
                indexes = np.append(indexes,np.arange(len(fd.get_q_values(d[0])), dtype=np.int16))
                N += len(files[f])
            
        indexes = np.sort(np.unique(indexes))
        
        print(indexes)
        
        self.__indexescombo.clear()
        self.__indexescombo.addItems(["q-index = %i"%i for i in indexes])
        self.__indexescombo.setCurrentIndex(0 if cindex == -1 else cindex)
                
        cindex = self.__indexescombo.currentIndex()
        if cindex == -1 or cindex >= len(indexes):
            logger.warning("cindex: %i, indexes: %s",cindex, str(indexes))
            cindex=0
            
        if len(indexes) == 0:
            return
        
        self.__canvas.setup(N, indexes[cindex], self.__colorbarscale.currentText(), self.__mincolorbar.value(), self.__maxcolorbar.value())
        
        j = 0
        for f,v in files.items():
            with XPCSResultFile(f) as fd:
                for k in v:
                    self.__canvas.plot(fd,k,j, self.__plottype.currentIndex(),
                                       self.__lagsparcification.currentData(), self.__Nlagresample.value(), 
                                       self.__agesparcification.currentData(), self.__Nageresample.value())
                    j += 1
            
        self.__canvas.draw()
        
        # Remove motion event, this just make the program freeze with that event
        while 'motion_notify_event' in self.__canvas.callbacks.callbacks:
            self.__canvas.callbacks.callbacks.pop('motion_notify_event')
    
    def clear(self):
        self.__canvas.clear()
        
        
class Canvas2tCorrelation(FigureCanvas):
    
    PLOT_TS_AGE_LOG = 0
    PLOT_TS_AGE_LIN = 1
    PLOT_XY         = 2
    
    NO_SPARCIFICATION = None
    LIN_SPARCIFICATION = "lin"
    LOG_SPARCIFICATION = "log"
    
    def __init__(self, parent=None, width=10, height=10, dpi=cmm.default_dpi):
        self.__fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        super().__init__(self.__fig)
        
        self.setMaximumHeight(100000)
        self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        
    def setup(self, N, qidx, cmapname='jet', cmin=.5, cmax=2):
        
        logger.debug([N, qidx])
        
        self.__qidx = qidx
        
        nCols = int(np.floor(N**0.5))
        nRows = int(np.ceil(N/nCols))
        
        gs = self.__fig.add_gridspec(nRows, nCols+1,width_ratios=[*[30]*nCols,1])
        
        self.__axes = []
        
        for y in range(nRows*nCols):
            self.__axes += [self.__fig.add_subplot(gs[y//nCols,y%nCols])]
                
        self.__axcb = self.__fig.add_subplot(gs[:,-1])
        
        self.__cmap = plt.get_cmap(cmapname)
        self.__norm = mpl.colors.Normalize(vmin=cmin, vmax=cmax)
        cb = self.__fig.colorbar(mpl.cm.ScalarMappable(norm=self.__norm, cmap=self.__cmap), cax=self.__axcb)        
        cb.set_label("$g_2$")
        
    def plot(self, file, k, j, plot_type = 0, lagsparse=None, lagN=0, agesparse=None, ageN=0):
        
            
        ax = self.__axes[j]
        
        try:
            ttcf, ts, age = file.get_ttcf(k, self.__qidx)
            
            logger.debug("Data read")
        except Exception as e:
            logger.warning(f"Unable to read TTCF\n{e}")
            return
        
        logger.debug(f"{ttcf.shape} {ts.shape} {age.shape}")
        logger.debug(f"{lagN}, {ageN}, {lagsparse}, {agesparse}")
        if lagsparse is not None or agesparse is not None:
            ts, age, ttcf = gt.ttcf_resample_npoints(ttcf, ts, age, lagN, ageN, lagsparse, agesparse)
            logger.debug((ttcf, ts, age))
            logger.debug(f"{ttcf.shape} {ts.shape} {age.shape}")
        
        logger.debug((np.sum(np.isnan(ts)), np.sum(np.isnan(age)),))
        
        mskage = ~np.isnan(age)
        msklag = ~np.isnan(ts)
        logger.debug(f"{ttcf.shape} {mskage.shape} {msklag.shape}")
        
        X,Y = np.meshgrid(ts[msklag], age[mskage])
        
        if plot_type == self.PLOT_XY:
#            dt = age[1]-age[0]
            ax.pcolormesh((.5*X+Y),(Y-.5*X),ttcf[mskage,:][:,msklag], cmap=self.__cmap, norm=self.__norm, rasterized=True)
            ax.pcolormesh((Y-.5*X),(.5*X+Y),ttcf[mskage,:][:,msklag], cmap=self.__cmap, norm=self.__norm, rasterized=True)
            
            ax.set_xlabel('$t_1 (s)$')
            ax.set_ylabel('$t_2 (s)$')
            
            ax.set_aspect('equal', 'box')
            ax.set_xlim([0,np.nanmax(age)])
            ax.set_ylim([0,np.nanmax(age)])
        else:
            ax.pcolormesh(X,Y,ttcf[mskage,:][:,msklag], cmap=self.__cmap, norm=self.__norm, rasterized=True, snap=True, shading='nearest')                
        
            if plot_type == self.PLOT_TS_AGE_LOG:
                ax.set_xscale('log')
                ts = ts[1:]
            else:
                ax.set_aspect('equal', 'box')
                
            ax.set_xlim([np.nanmin(ts),np.nanmax(ts)])
            ax.set_ylim([0,np.nanmax(age)])
            
            ax.set_xlabel(r'Lag time $\tau~(s)$')
            ax.set_ylabel(r'Age $t~(s)$')
        
        qs = file.get_q_values(file.analysis_keys[0])
        
        ax.set_title('%s %s %s q=%.3e'%(file.title, file.filename, k, qs[self.__qidx-1]), fontsize=cmm.default_title_font_size)
        
    def clear(self):
        self.__fig.clf()


