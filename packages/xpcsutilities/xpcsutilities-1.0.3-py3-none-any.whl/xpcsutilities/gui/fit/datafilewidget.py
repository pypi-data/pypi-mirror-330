# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import PyQt5.QtWidgets as qtw

import numpy as np
import logging
logger = logging.getLogger(__name__)

from xpcsutilities.tools.result_file import XPCSResultFile
        

class DataFileModel(qtg.QStandardItemModel):
    def __init__(self, files):
        
        logger.debug(files)
        
        super().__init__()
        
        self.__items = dict()
        
        for fnam, v in files.items():
            with XPCSResultFile(fnam) as f:
                itf = qtg.QStandardItem(f.filename)
                itf.setCheckable(True)
                itf.setCheckState(qtc.Qt.Checked)
                
                self.__items[f.filename] = {'__main__': itf}
                
#                qs = f.q_ranges
                
                for k in v:
                    qs = f.get_q_values(k)
                    
                    itk = qtg.QStandardItem(k)
                    itk.setCheckable(True)
                    itk.setCheckState(qtc.Qt.Checked)
                    
                    self.__items[f.filename][k] = {'__main__': itk}
                    
                    for qid, q in enumerate(qs):
                        itq = qtg.QStandardItem("%.0f (%.02e)"%(qid,q))
                        itq.setCheckable(True)
                        itq.setCheckState(qtc.Qt.Checked)
            
                        itk.appendRow(itq)
                        self.__items[f.filename][k][qid] = itq
                        
                    itf.appendRow(itk)
            self.appendRow(itf)
            
    def isActive(self, filename, key=None, qid=None):
#        print(filename, key, qid)
#        print(self.__items[filename]['__main__'].checkState())
#        if key is not None:
#            print(self.__items[filename][key]['__main__'].checkState())
#            if qid is not None:
#                print(self.__items[filename][key][qid].checkState())
                
        if filename in self.__items:
            if key is None:
                return self.__items[filename]['__main__'].checkState() != qtc.Qt.Unchecked
            elif key in self.__items[filename]:
                if qid is None:
                    return self.__items[filename][key]['__main__'].checkState() != qtc.Qt.Unchecked
                elif qid in self.__items[filename][key]:
                    return self.__items[filename][key][qid].checkState() != qtc.Qt.Unchecked
        
        return False
    


class DataFileWidget(qtw.QGroupBox):
    def __init__(self):
        super().__init__("Data selection")
        
        self.__layout = qtw.QFormLayout()
        self.setLayout(self.__layout)
        
        self.__datalsttree = qtw.QTreeView()
        self.__datalsttree.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)
        self.__layout.addRow(self.__datalsttree)
        
        self.__btnCheckSelected = qtw.QPushButton("Check selected lines")
        self.__btnCheckSelected.clicked.connect(self.onCheckSelected)
        
        self.__btnUncheckSelected = qtw.QPushButton("Uncheck selected lines")
        self.__btnUncheckSelected.clicked.connect(self.onUncheckSelected)
        self.__layout.addRow(self.__btnCheckSelected, self.__btnUncheckSelected)
        
        self.__btnCheckOnlySelected = qtw.QPushButton("Check only selected lines")
        self.__btnCheckOnlySelected.clicked.connect(self.onCheckOnlySelected)
        
        self.__btnUncheckOnlySelected = qtw.QPushButton("Uncheck only selected lines")
        self.__btnUncheckOnlySelected.clicked.connect(self.onUncheckOnlySelected)
        self.__layout.addRow(self.__btnCheckOnlySelected, self.__btnUncheckOnlySelected)
        
        self.__data = dict()
        
    def onCheckSelected(self):
        """
        Check the selected lines
        """
        idxs = self.__datalsttree.selectedIndexes()
        
        for idx in idxs:
            it = self.__model.itemFromIndex(idx)
            it.setCheckState(qtc.Qt.Checked)
            
    def onUncheckSelected(self):
        """
        Uncheck the selected lines
        """
        idxs = self.__datalsttree.selectedIndexes()
        
        for idx in idxs:
            it = self.__model.itemFromIndex(idx)
            it.setCheckState(qtc.Qt.Unchecked)
            
    def checkWithParent(self, it : qtg.QStandardItem ):
        """
        Check parent item, recursively
        """
        
        it.setCheckState(qtc.Qt.Checked)
        
        if it.parent() is not None:
            self.checkWithParent(it.parent())
            
    def onCheckOnlySelected(self):
        """
        Check the only selected lines, all other are unchecked
        """
        idxs = self.__datalsttree.selectedIndexes()
        
        self.__datalsttree.selectAll()
        self.onUncheckSelected()
        self.__datalsttree.clearSelection()
        
        for idx in idxs:
            it = self.__model.itemFromIndex(idx)
            self.checkWithParent(it)
            self.__datalsttree.selectionModel().select(idx, qtc.QItemSelectionModel.Select)
            
    def onUncheckOnlySelected(self):
        """
        Uncheck only the selected lines, all other are checked
        """
        idxs = self.__datalsttree.selectedIndexes()
        
        self.__datalsttree.selectAll()
        self.onCheckSelected()
        self.__datalsttree.clearSelection()
        
        for idx in idxs:
            it = self.__model.itemFromIndex(idx)
            it.setCheckState(qtc.Qt.Unchecked)
            self.__datalsttree.selectionModel().select(idx, qtc.QItemSelectionModel.Select)
        
    def setModel(self, model : DataFileModel = None):
        self.__model = model if model is not None else DataFileModel({})
        self.__datalsttree.setModel(model)
        
    def clearFiles(self):
        self.__datas = dict()
        self.setModel()
        
    def loadFiles(self, files):
        logger.debug(files)
        # Display curves selector
        self.setModel(DataFileModel(files))
        self.__data = dict()
        
        # Load datas
        for fnam, v in files.items():
            with XPCSResultFile(fnam) as f:
                self.__datas[f.filename] = dict()
                
                for k in f.analysis_keys:
                    lag, cf, stde = f.get_correlations(k)
                    qs = f.get_q_values(k)
                    
                    self.__datas[f.filename][k] = { 'lag': lag,
                                                    'cf': cf,
                                                    'ts': f.timestamp,
                                                    'stde': stde,
                                                    'qidx': [i for i in range(len(qs))],
                                                    'qs': qs }
    
    def getSelectedDatas(self):
        resdata = []
            
        # Load selected data
        NROWS = 0
    
        mints = +np.inf
        
        for fn,datf in self.__datas.items():
            if self.__model.isActive(fn):
                for k, datk in datf.items():
                    if datk['ts'] is not None and datk['ts'] < mints:
                        mints = datk['ts']
        
        for fn,datf in self.__datas.items():
            if self.__model.isActive(fn):
                for k, datk in datf.items():
                    if self.__model.isActive(fn, k):
                        qidx = []
                        qs = []
                        jidx = []
                        j=0
                        for i,qid in enumerate(datk['qidx']):
                            if self.__model.isActive(fn,k,qid):
                                jidx += [i,]
                                qidx += [qid,]
                                qs += [datk['qs'][i],]
                                j += 1
                                NROWS += 1
                                
                                
                        resdata += [{'filename': fn,
                                     'direction': k,
                                     'ts': datk['ts'],
#                                     'tsr': datk['ts']-mints,
                                     'q-index': qidx,
                                     'qs': qs,
                                     'lag': datk['lag'].ravel(),
                                     'cf': datk['cf'][jidx,:],
                                     'fitres': dict()}, ]
                    
        return resdata, NROWS
        
        
        
    