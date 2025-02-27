# -*- coding: utf-8 -*-



import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtWidgets as qtw

import numpy as np
import scipy.optimize as opt

import traceback
import logging
logger = logging.getLogger(__name__)

from .datafilewidget import DataFileModel, DataFileWidget
import xpcsutilities.tools.graphs as gt
from .resultgraph import ResultFitGraph, ResultParamsFitGraph
from .curvefitwidget import CurveFitWidget

class FitTab(qtw.QWidget):
    
    OPT_COLOR_Q     = 0
    OPT_COLOR_QIDX  = 1
    OPT_COLOR_TIME  = 2
    
    def __init__(self):
        super().__init__()
        
        #Layout
        self.__layout = qtw.QGridLayout()
        self.__layout.setColumnStretch(0,1)
        self.__layout.setColumnStretch(1,3)
        self.setLayout(self.__layout)
        
        # File list
        self.__dataList = DataFileWidget()
        self.__layout.addWidget(self.__dataList, 0,0)
        
        # Contrast rescaling
        self.__con_rescale = qtw.QGroupBox("Rescale contrast before fitting")
        self.__layout.addWidget(self.__con_rescale,1,0)
        self.__con_rescale.setCheckable(True)
        self.__con_rescale.setChecked(True)
        self.__con_rescale.toggled.connect(self.__onContrastRescaleChanged)
        
        self.__con_rescale_layout = qtw.QFormLayout()
        self.__con_rescale.setLayout(self.__con_rescale_layout)
        
        self.__con_rescale_method = qtw.QComboBox()
        self.__con_rescale_layout.addRow("Rescaling method", self.__con_rescale_method)
        
        self.__con_rescale_method.addItem("Average")
        self.__con_rescale_method.addItem("Fit linear")
        self.__con_rescale_method.addItem("Fit exponential")
        
        self.__con_rescale_method.setCurrentIndex(1)
        
        self.__con_rescale_limit = qtw.QDoubleSpinBox()
        self.__con_rescale_layout.addRow("Maximum lag time", self.__con_rescale_limit)
        self.__con_rescale_limit.setDecimals(6)
        self.__con_rescale_limit.setMaximum(np.inf)
        self.__con_rescale_limit.setValue(0.0035)
        
        # Curve fitting
        self.__curve_fit_widget = CurveFitWidget()
        self.__layout.addWidget(self.__curve_fit_widget,2,0)
        self.__curve_fit_widget.setCheckable(True)
        self.__curve_fit_widget.setChecked(True)
                        
        # Results         
        self.__tabreswidget = qtw.QTabWidget()
        self.__tabreswidget.setTabsClosable(True)
        self.__tabreswidget.tabCloseRequested.connect(self.__onTabCloseRequested)
        self.__layout.addWidget(self.__tabreswidget,0,1,4,1)
        
        w = qtw.QWidget()
        self.__reslayout = qtw.QVBoxLayout()
        w.setLayout(self.__reslayout)
        self.__tabreswidget.addTab(w, "Results" )
        
        self.__tabrestable = qtw.QTableWidget()
        header = self.__tabrestable.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeToContents)
        self.__reslayout.addWidget(self.__tabrestable)
        
        self.__optlayout = qtw.QHBoxLayout()
        self.__reslayout.addLayout(self.__optlayout)
        
        self.__opt1layout = qtw.QFormLayout()
        self.__optlayout.addLayout(self.__opt1layout)
        
        self.__optgroupbyfile = qtw.QCheckBox()
        self.__optgroupbyfile.setChecked(True)
        self.__opt1layout.addRow("Separate each files", self.__optgroupbyfile)
        
        self.__optgroupbydir = qtw.QCheckBox()
        self.__optgroupbydir.setChecked(True)
        self.__opt1layout.addRow("Separate each direction", self.__optgroupbydir)
        
        self.__optgroupbyqid = qtw.QCheckBox()
        self.__optgroupbyqid.setChecked(False)
        self.__opt1layout.addRow("Separate each q-index", self.__optgroupbyqid)
        
        self.__optcolorby = qtw.QComboBox()
        self.__opt1layout.addRow("Color", self.__optcolorby)
        
        self.__optcolorby.insertItem(self.OPT_COLOR_Q, 'q')
        self.__optcolorby.insertItem(self.OPT_COLOR_QIDX, 'q index')
        self.__optcolorby.insertItem(self.OPT_COLOR_TIME, 'time')
        
        self.__fitsavebtn = qtw.QPushButton("Save results")
        self.__fitsavebtn.setMinimumHeight(100)
        self.__optlayout.addWidget(self.__fitsavebtn)
        self.__fitsavebtn.clicked.connect(self.savefit)
        
        self.__fitdisplaybtn = qtw.QPushButton("Display selected results")
        self.__fitdisplaybtn.setMinimumHeight(100)
        self.__optlayout.addWidget(self.__fitdisplaybtn)
        self.__fitdisplaybtn.clicked.connect(self.displayfit)
        
        self.__fitdisplayparamsbtn = qtw.QPushButton("Display parameters")
        self.__fitdisplayparamsbtn.setMinimumHeight(100)
        self.__optlayout.addWidget(self.__fitdisplayparamsbtn)
        self.__fitdisplayparamsbtn.clicked.connect(self.displayfitparams)
        
        # Button
        self.__btnlayout = qtw.QHBoxLayout()
        self.__layout.addLayout(self.__btnlayout,3,0)
        
        self.__inibtn = qtw.QPushButton("Display  curves with initial values")
        self.__inibtn.setMinimumHeight(100)
        self.__btnlayout.addWidget(self.__inibtn)
        self.__inibtn.clicked.connect(self.initdisplay)
        
        self.__fitbtn = qtw.QPushButton("Fit")
        self.__fitbtn.setMinimumHeight(100)
        self.__btnlayout.addWidget(self.__fitbtn)
        self.__fitbtn.clicked.connect(self.fit)
        
    def __onTabCloseRequested(self, idx : int):
        if idx == 0:
            return
        
        self.__tabreswidget.removeTab(idx)
        
    def __onContrastRescaleChanged(self):
        self.__curve_fit_widget.setFitContrast(not self.__con_rescale.isChecked())
        
    def clear(self):
        self.__dataList.clearFiles()
        
    def plot(self, files):
        logger.debug(files)
        self.__dataList.loadFiles(files)
                
    def initdisplay(self):
        
        fnc, parval = self.__curve_fit_widget.fitfunction()
        pars = self.__curve_fit_widget.args2params(1,parval, *self.__curve_fit_widget.initValues(1))
        
        logger.debug(parval)
        logger.debug(pars)
        
        sepfile = self.__optgroupbyfile.isChecked()
        sepdir = self.__optgroupbydir.isChecked()
        sepqid = self.__optgroupbyqid.isChecked()
        
        resd = dict()
        
        minc = +np.inf
        maxc = -np.inf
        
        mints = +np.inf
                        
        seldata, NROWS = self.__dataList.getSelectedDatas()
            
        for d in seldata:
            for i, qid in enumerate(d['q-index']):
                key = ""
                if sepfile:
                    key += "__fn__"+d['filename']
                if sepdir:
                    key += "__dir__"+d['direction']
                if sepqid:
                    key += "__qid__%i"%qid
                    
                if key not in resd:
                    resd[key] = []
                    
                if self.__optcolorby.currentIndex() == self.OPT_COLOR_Q:
                    colv = d['qs'][i]
                elif self.__optcolorby.currentIndex() == self.OPT_COLOR_QIDX:
                    colv = qid
                elif self.__optcolorby.currentIndex() == self.OPT_COLOR_TIME:
                    colv = d['ts'] - mints
                
                if colv > maxc: maxc = colv
                if colv < minc: minc = colv
                    
                resd[key] += [{'filename': d['filename'],
                               'direction': d['direction'],
                               'ts': d['ts'],
                               'tsr': d['tsr'],
                               'q-index': qid,
                               'color': colv,
                               'q': d['qs'][i],
                               'lag': d['lag'].ravel(),
                               'cf': d['cf'][i,:],
                               'fitres': pars.copy(),
                               'fitkeys': pars.keys(),
                               'fitfun': fnc},]
    
        (cmapi, normi, mv) = gt.qindex_colors([minc, maxc])
    
        try:
            # Get contrast
            if self.__con_rescale.isChecked():
                for k,r in resd.items():
                    for l in r:
                        lag = l['lag']
                        msk = lag < self.__con_rescale_limit.value()
                        lag = lag[msk]
                        cf = l['cf'][msk]
                        
                        beta = None
                        
                        if self.__con_rescale_method.currentIndex() == 0: # Average
                            beta = np.mean(cf)-1.
                        elif self.__con_rescale_method.currentIndex() == 1: # Linear fit
                            k = np.polyfit(lag, cf, 1)
                            beta = k[1]-1.
                        elif self.__con_rescale_method.currentIndex() == 2: # Exp fit
                            fun = lambda lt, k0, tau: k0*np.exp(-lt/tau)+1.
                            k = opt.curve_fit(fun, lag, cf, [ 0.4, 1e-2 ], bounds=([ 0, 0 ], [ 1, +np.inf ]))
                            beta = k[0][0]
                        l['fitres']['beta'] = beta
            
            #print(resd)
            
            i=0
            for k,res in resd.items():
                fitw = ResultFitGraph(res, cmapi, normi)
                self.__tabreswidget.addTab(fitw, "Init %i"%i)
                i += 1
            
            self.__tabreswidget.setCurrentIndex(self.__tabreswidget.count()-1)
        except Exception as e:
            logger.fatal(traceback.format_exc())
            qtw.QMessageBox.critical(self, "Error", str(e))
                
    def fit(self):
        try:
            self.__resdata, NROWS = self.__dataList.getSelectedDatas()
                                    
            if len(self.__resdata) == 0:
                logger.warning("No data to fit")
                return
            
            # Contrast
            if self.__con_rescale.isChecked():
                for i,l in enumerate(self.__resdata):
                    lag = l['lag'].ravel()
                    msk = lag < self.__con_rescale_limit.value()
                    
                    beta = np.empty((len(l['q-index']),), np.float32)
                    
                    for j, qid in enumerate(l['q-index']):
                        if self.__con_rescale_method.currentIndex() == 0: # Average
                            beta[j] = np.mean(l['cf'][j,msk])-1.
                        elif self.__con_rescale_method.currentIndex() == 1: # Linear fit
                            
                            logger.debug((l['cf'].shape, j, msk.shape))
                            
                            cf = l['cf'][j,msk]
                            
                            k = np.polyfit(lag[msk], cf, 1)
                            beta[j] = k[1]-1.
                        elif self.__con_rescale_method.currentIndex() == 2: # Exp fit
                            cf = l['cf'][j,msk]
                            k = opt.curve_fit(lambda lt, k0, tau: k0*np.exp(-lt/tau)+1., lag[msk], cf, [ 0.4, 1e-2 ], bounds=([ 0, 0 ], [ 1, +np.inf ]))
                            beta[j] = k[0][0]
                    
                    l['fitres']['beta'] = beta 
                        
            # Curve fitting
            if self.__curve_fit_widget.isChecked():
                for i,l in enumerate(self.__resdata):
                    fun, parv = self.__curve_fit_widget.fitfunction()
                    keys = parv.keys()
                    
                    fitfnc = lambda t, *args: fun(t, np.array(l['qs']), *args).ravel()
                    
                    l['fitfun'] = fun
                    l['fitkeys'] = keys
                    
                    msk = l['lag'] < self.__curve_fit_widget.maxlag()
                    
                    if self.__con_rescale.isChecked():
                        cf =  (l['cf'].T-1.)/l['fitres']['beta']
                    else:
                        cf = l['cf'].T-1.
                    
                    n = len(l['qs'])
                    
                    # WARNING: keep initValues to 1 because the scaling is done in args2params according to initial values
                    
                    initv = self.__curve_fit_widget.initValues(n)
                    bounds = self.__curve_fit_widget.bounds(n)
                    
                    logger.debug("Fit initial value: "+str(initv))
                    logger.debug("Fit bounds: "+str(bounds))
                    
                    msk[0] = False
                    
                    msk = np.logical_and(msk, np.sum(~np.isfinite(cf), axis=1) == 0)
                    
                    kopt = opt.curve_fit(fitfnc,
                                         l['lag'][msk], cf[msk,:].ravel(),
                                         initv,
                                         bounds=bounds,
                                         method='dogbox',
                                         verbose=0,
                                         loss='linear', # linear ( default, soft_1l, cauchy )
                                         ftol=1e-12,
                                         gtol=1e-12,
                                         xtol=1e-12,
                                         )
                    
                    logger.debug(kopt[1])
                    logger.debug(parv)
                    logger.debug(n)
                    
                    params = self.__curve_fit_widget.args2params(n, parv, *kopt[0])
                    
                    logger.debug(params)
                    
                    for k,v in params.items():
                        l['fitres'][k] = v
                        
                    
        except Exception as e:
            logger.fatal(traceback.format_exc())
            qtw.QMessageBox.critical(self, "Error", str(e))
                    
        # Display results to table
        self.__tabrestable.setColumnCount(5+len( self.__resdata[0]['fitres'].keys()))
        self.__tabrestable.setRowCount(NROWS)
        self.__tabrestable.setHorizontalHeaderLabels(['','filename','direction','q-index','q', *self.__resdata[0]['fitres'].keys()])
        
        self.__tabreswidget.setCurrentIndex(0)
        
        i=0
        for l in self.__resdata:
            l['check'] = []
            for m in range(len(l['q-index'])):
                chkbx = qtw.QCheckBox()
                chkbx.setChecked(True)
                l['check'] += [chkbx, ]
                self.__tabrestable.setCellWidget(i,0,chkbx)
                self.__tabrestable.setItem(i,1,qtw.QTableWidgetItem(l['filename']))
                self.__tabrestable.setItem(i,2,qtw.QTableWidgetItem(l['direction']))
                self.__tabrestable.setItem(i,3,qtw.QTableWidgetItem("%i"%l['q-index'][m]))
                self.__tabrestable.setItem(i,4,qtw.QTableWidgetItem("%.3e"%l['qs'][m]))
                
                for j,k in enumerate(l['fitres'].keys()):
                    self.__tabrestable.setItem(i,j+5,qtw.QTableWidgetItem('%.3e'%l['fitres'][k][m]))
                    
                i += 1
                
    @property
    def strModel(self):
        """
        Return the current model as string
        """
        return "1+beta*(%s)"%self.__curve_fit_widget.strModel()
                
    def savefit(self):
        """
        Save the results in table to csv file
        """
        
        outf = qtw.QFileDialog.getSaveFileName(self, "Save file to", "results.csv")
        outf = outf[0]
        
        if outf == '':
            return
        
        with open(outf, 'w') as fd:
            
            fd.write("# model; g1 = %s\n"%(self.strModel))
            fd.write("## filename;direction;q-index;q (A^-1);%s\n"%(';'.join(self.__resdata[0]['fitres'].keys())))
            
            for l in self.__resdata:
                for m in range(len(l['q-index'])):
                    fd.write(l['filename']+';')
                    fd.write(l['direction']+';')
                    fd.write("%i"%l['q-index'][m]+';')
                    fd.write("%.3e"%l['qs'][m]+';')
                    
                    for j,k in enumerate(l['fitres'].keys()):
                        fd.write('%.3e'%l['fitres'][k][m]+';')
                        
                    fd.write('\n')
                    
    
    def displayfit(self):
        """
        Display the correlation function curve together with fit curve
        """
        
        sepfile = self.__optgroupbyfile.isChecked()
        sepdir = self.__optgroupbydir.isChecked()
        sepqid = self.__optgroupbyqid.isChecked()
        
        resd = dict()
        
        minc = +np.inf
        maxc = -np.inf
        
        for r in self.__resdata:
            for i,qid in enumerate(r['q-index']):
                if not r['check'][i].isChecked():
                    continue
                
                key = ""
                if sepfile:
                    key += "__fn__"+r['filename']
                if sepdir:
                    key += "__dir__"+r['direction']
                if sepqid:
                    key += "__qid__%i"%qid
                    
                if key not in resd:
                    resd[key] = []
                    
                
                                    
                if self.__optcolorby.currentIndex() == self.OPT_COLOR_Q:
                    colv = r['qs'][i]
                elif self.__optcolorby.currentIndex() == self.OPT_COLOR_QIDX:
                    colv = r['q-index'][i]
                elif self.__optcolorby.currentIndex() == self.OPT_COLOR_TIME:
                    colv = r['tsr']
                                
                if colv > maxc: maxc = colv
                if colv < minc: minc = colv
                    
                rl = r.copy()
                del rl['check']
                rl['color'] = colv
                rl['q-index'] = r['q-index'][i]
                rl['q'] = r['qs'][i]
                rl['cf'] = rl['cf'][i,:]
                
                rl['fitres'] = dict()
                for k in r['fitres'].keys():
                    rl['fitres'][k] = r['fitres'][k][i]
                    
                resd[key] += [rl,]
        
        (cmapi, normi, mv) = gt.qindex_colors([minc, maxc])
        i=0
        for k,res in resd.items():
            fitw = ResultFitGraph(res, cmapi, normi)
            self.__tabreswidget.addTab(fitw, "Graph %i"%i)
            i += 1
            
        self.__tabreswidget.setCurrentIndex(self.__tabreswidget.count()-1)
        
    def displayfitparams(self):
        """
        Display the correlation function curve together with fit curve
        """
        
        sepfile = self.__optgroupbyfile.isChecked()
        sepdir = self.__optgroupbydir.isChecked()
        sepqid = self.__optgroupbyqid.isChecked()
        
        resd = dict()
        
        for r in self.__resdata:
            for i,qid in enumerate(r['q-index']):
                if not r['check'][i].isChecked():
                    continue
                
                key = ""
                if sepfile:
                    key += "__fn__"+r['filename']
                if sepdir:
                    key += "__dir__"+r['direction']
                if sepqid:
                    key += "__qid__%i"%qid
                    
                if key not in resd:               
                    resd[key] = {'q'        : [],
                                 'tsr'      : [],
                                 'dir'      : [],
                                 'file'     : [],
                                 'params'   : {k:[] for k in r['fitres']} }
                    
                resd[key]['q'] += [ r['qs'][i], ]
                resd[key]['tsr'] += [ r['tsr'], ]
                resd[key]['dir'] += [ r['direction'], ]
                resd[key]['file'] += [ r['filename'], ]
                
                for k in r['fitres']:
                    resd[key]['params'][k] += [ r['fitres'][k][i], ]
        
        i=0
        for k,res in resd.items():
            fitw = ResultParamsFitGraph(res)
            self.__tabreswidget.addTab(fitw, "Params %i"%i)
            i += 1
            
        self.__tabreswidget.setCurrentIndex(self.__tabreswidget.count()-1)

