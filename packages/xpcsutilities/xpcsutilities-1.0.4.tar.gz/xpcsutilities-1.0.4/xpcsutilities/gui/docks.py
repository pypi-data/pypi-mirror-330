#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 13:29:26 2021

@author: opid02
"""

import numpy as np
import logging
import PyQt5.QtGui as qtg
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import os
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler
from xpcsutilities.tools.result_file import XPCSResultFile, NotXPCSFileException

logger = logging.getLogger(__name__)


class FileDatabase(object):
    """
    File database
    """
    __db = dict()
    __rdb = dict()
    
    class FileDescriptor(object):
        """
        Describe a file
        """
        
        def __init__(self, filename):
            """
            Read the filename and fill the cache fields
            """
            
            filename = os.path.abspath(filename)
            
            with XPCSResultFile(filename) as fd:
                self.__filename = filename
                self.__keys = fd.analysis_keys
                self.__title = fd.title
                
        @property
        def filename(self):
            return self.__filename
        
        @property
        def keys(self):
            return self.__keys
        
        @property
        def title(self):
            return self.__title
    
    @classmethod
    def getDescriptorFromFilename(cls, filename):
        """
        Return a file descriptor based on filename, creating a new one if needed
        """
        
        if filename not in cls.__db:
            cls.__db[filename] = cls.FileDescriptor(filename)
                
        return cls.__db[filename]
        
    
    @classmethod
    def getItemsFromFilename(cls, filename):
        """
        Create items for filename entries if needed
        """
        
        fd = cls.getDescriptorFromFilename(filename)
        
        if fd is None:
            return None
            
        r = dict()
        
        for k in fd.keys:
            uid = f"{fd.filename}::{k}"
            
            if not uid in cls.__rdb:                
                cls.__rdb[uid] = {'fd': fd, 'key': k}
                
            r[uid] = cls.__rdb[uid]
            
        return r
            
    @classmethod
    def getDescriptorFromKey(cls, uid):
        """
        Return the entry from the item key
        """
        
        if uid in cls.__rdb:
            return cls.__rdb[uid]
        
        raise ValueError(f"Item {uid} not found in database")


class FileDock(qtw.QDockWidget):
    # Signals
    onPlotRequest = qtc.pyqtSignal(dict)
    
    def __init__(self):
        logger.debug("FileDock creation")
        super().__init__()
        self.__currentDir = os.getcwd()
        
        w = qtw.QWidget()
        self.__layout = qtw.QVBoxLayout()
        w.setLayout(self.__layout)
        self.setWidget(w)
        
        # Change directory button
        self.__btnSetFolder = qtw.QPushButton("Set working folder")
        self.__btnSetFolder.clicked.connect(self.setWorkingFolder)
        
        self.__layout.addWidget(self.__btnSetFolder)
        
        # File filter
        self.__filefilter = qtw.QLineEdit("*.h5")
        self.__filefilter.editingFinished.connect(lambda *args: self.setWorkingFolder(self.__currentDir))
        self.__layout.addWidget(self.__filefilter)
        
        # File list
#        self.__filelist = qtw.QListWidget()
#        self.__filelist.setSelectionMode(qtw.QListWidget.ExtendedSelection)
#        self.__layout.addWidget(self.__filelist)
        self.__filelist = qtw.QTreeView()
        
        self.__filemodel = qtg.QStandardItemModel()
        self.__filemodel.setColumnCount(3)
        self.__filemodel.setHeaderData(0, qtc.Qt.Horizontal, 'File')
        self.__filemodel.setHeaderData(1, qtc.Qt.Horizontal, 'Entry')
        self.__filemodel.setHeaderData(2, qtc.Qt.Horizontal, 'Title')
        # self.__filemodel.setHorizontalHeaderLabels(['File', 'Entry'])
        
        self.__filelist.setModel(self.__filemodel)
        self.__filelist.setSelectionMode(qtw.QListWidget.ExtendedSelection | qtw.QListWidget.SelectRows)
        self.__layout.addWidget(self.__filelist)
        
        # ProgressBar
        self.__prgBar = qtw.QProgressBar()
        self.__prgBar.setMinimum(0)
        self.__layout.addWidget(self.__prgBar)
        
        # Update list
        self.__upbtn = qtw.QPushButton("Update List")
        self.__upbtn.setMinimumHeight(50)
        self.__layout.addWidget(self.__upbtn)
        self.__upbtn.clicked.connect(self.updateFiles)
        
        # Plot button
        self.__pltbtn = qtw.QPushButton("Plot")
        self.__pltbtn.setMinimumHeight(100)
        self.__layout.addWidget(self.__pltbtn)
        self.__pltbtn.clicked.connect(self.onPlotButtonPressed)
        
        # File observer
        self.__observer = PollingObserver()
        self.__observer.start()
        
        # Load from current directory
        self.__lastDir = None
        self.__currfiles = dict()
        
        self.setMinimumWidth(400)
        
        
        # self.setWorkingFolder(os.getcwd())
        qtc.QTimer.singleShot(1000, lambda: self.setWorkingFolder(os.getcwd()))
        
        
    def __del__(self):
        self.__observer.stop()
        self.__observer.join()
    
    @property
    def fileFilters(self):
        t = self.__filefilter.text()
        
        if t.strip() == '':
            return ['*',]
        else:
            return [ f.strip() for f in self.__filefilter.text().split(',')]
        
    def setWorkingFolder(self, wd=None):
        
        if not wd:
            nd = qtw.QFileDialog.getExistingDirectory(self, "Change working directory", self.__currentDir, qtw.QFileDialog.ShowDirsOnly)
            if os.path.isdir(nd):
                self.__currentDir = nd
            else:
                logger.warning('Non existant directory: %s', nd)
                return
        else:
            self.__currentDir = wd
            
        os.chdir(self.__currentDir)
            
        self.updateFiles()
        
        # Watch for modifications in the folder
#        ignore_patterns = None
#        ignore_directories = True
#        case_sensitive = True
        
#        event_handler = PatternMatchingEventHandler(self.fileFilters, ignore_patterns, ignore_directories, case_sensitive)
#        event_handler.on_created = lambda *args, **kwargs: self.updateFiles()
#        event_handler.on_deleted = lambda *args, **kwargs: self.updateFiles()
#        event_handler.on_modified = lambda *args, **kwargs: self.updateFiles()
#        event_handler.on_moved = lambda *args, **kwargs: self.updateFiles()
#        
#        self.__observer.unschedule_all()
#        self.__observer.schedule(event_handler, self.__currentDir, recursive=False)
        
    def updateFiles(self):
        
        logger.debug("Load files from directory %s", self.__currentDir)
        
        #self.__filemodel.clear()
#        self.__filemodel.setColumnCount(2)
#        self.__filemodel.setHeaderData(0, qtc.Qt.Horizontal, 'File')
#        self.__filemodel.setHeaderData(1, qtc.Qt.Horizontal, 'Entry')
        
        Files = []
        to_add = []
        to_delete = []
        rows_to_delete = []
        
        filelst = qtc.QDir(self.__currentDir).entryList(self.fileFilters, qtc.QDir.Files | qtc.QDir.Readable)
        Nf = len(filelst)
        self.__prgBar.setMaximum(Nf+10)
        
        for i,f in enumerate(filelst):
            f = os.path.abspath(f)
            logger.debug(f)
            Files += [f,]
#                Files[f] = FileDatabase.getItemsFromFilename(f)
            if f not in self.__currfiles:
                to_add += [f]
                
            self.__prgBar.setValue(i+1)
                
        
        for f,v in self.__currfiles.items():
            if f not in Files and v is not None:
                to_delete += [f]
                
                for it in v:
                    rows_to_delete += [ it.row(), ]
                        
        rows_to_delete.sort(reverse=True)
        
        
        self.__prgBar.setValue(Nf+2)

        for f in to_delete:
            del self.__currfiles[f]
            
        self.__prgBar.setValue(Nf+3)
            
        for r in rows_to_delete:
            self.__filemodel.removeRow(r)
            
        self.__prgBar.setValue(Nf+4)
                
        for i,f in enumerate(to_add):
            try:
                fd = FileDatabase.getItemsFromFilename(f)
            except NotXPCSFileException: # Skip non-XPCS files
                self.__currfiles[f] = None
                continue
            except Exception as e: # This might come because processing is not finished.
                logger.info(f"Problem with {f} {e}")
                continue
                
            for uid, v in fd.items():
                it1 = qtg.QStandardItem(os.path.basename(v['fd'].filename))
                it2 = qtg.QStandardItem(v['key'])
                it3 = qtg.QStandardItem(v['fd'].title)
                
                its = [it1, it2, it3]
                
                for it in its:
                    it.setData(uid)
                    it.setEditable(False);
                
                self.__filemodel.appendRow( its )
                
                if f not in self.__currfiles:
                    self.__currfiles[f] = []
                
                self.__currfiles[f] += [it1,]
                
            v = int(np.ceil(6./len(to_add)*i))
            self.__prgBar.setValue(Nf+4+v)
        
        self.__prgBar.setValue(Nf+10)
        self.__filelist.header().setStretchLastSection(True)
        self.__filelist.resizeColumnToContents(0)
        
        logger.debug("files to add: \n %s"%"\n  ".join(to_add))
        logger.debug("files to delete: \n %s"%"\n  ".join(to_delete))
#        logger.debug("_currfiles state: \n %s"%"\n  ".join([f"{k} : {v}" for k,v in self.__currfiles.items()]))
        
        logger.debug("Files loaded")
            
    def onPlotButtonPressed(self):
        self.onPlotRequest.emit(self.filesSelected)
    
    @property
    def filesSelected(self):
        r = dict()
        
        for s in self.__filelist.selectedIndexes():
            it = self.__filemodel.itemFromIndex(s)
            
            dbe = FileDatabase.getDescriptorFromKey(it.data())
            logger.debug(dbe)
            
            fn = dbe['fd'].filename
            en = dbe['key']
            
            if fn not in r:
                r[fn] = []
                
            if en not in r[fn]:
                r[fn] += [en,]
        
        logger.debug(r)
            
        return r
        
        
        
