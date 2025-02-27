#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 12:03:53 2021

@author: opid02
"""
import traceback
import logging
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc
import PyQt5.QtGui as qtg
import xpcsutilities.gui.docks as docks
import xpcsutilities.gui.contin.tab_contin as contin
import xpcsutilities.gui.graphs as graphs
import xpcsutilities.gui.fit as fit
from xpcsutilities.gui.export.dialog import XPCSExportDialog
from xpcsutilities.tools.result_file import XPCSResultFile

logger = logging.getLogger(__name__)

import pathlib

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(qtg.QIcon('%s/../xpcsutilities-logo.svg'%
pathlib.Path(__file__).parent.resolve()))
        self.setWindowTitle("XPCSUtilities 1.0")
        
        # Main widgets
        self.__mainwidget = qtw.QTabWidget()
        self.setCentralWidget(self.__mainwidget)
        
        self.__graphsWidgets = []
        
        # Menu
        self.__fileMenu = self.menuBar().addMenu("File")
        
        # File menu
        self.__fileMenu.addAction("Export selected files to ASCII", self.exportDialog)
        
        #Create graph views
        
        #SAXS 1D
        gsaxs = graphs.GraphSAXSWithQRange()
        self.__graphsWidgets += [gsaxs, ]
        self.__mainwidget.addTab(gsaxs, "SAXS 1D")
        
        # SAXS 2D
        g2saxs = graphs.GraphSAXSPattern()
        self.__graphsWidgets += [g2saxs, ]
        self.__mainwidget.addTab(g2saxs, "SAXS 2D")
        
        # 1time correlations
        gcorr = graphs.GraphCorrelation()
        self.__graphsWidgets += [gcorr, ]
        self.__mainwidget.addTab(gcorr, "Correlations")
        
        # 2time correlations
        g2corr = graphs.Graph2tCorrelation()
        self.__graphsWidgets += [g2corr, ]
        self.__mainwidget.addTab(g2corr, "TTCF")
                                 
        # Fitting tab
        g2fit = fit.FitTab()
        self.__graphsWidgets += [g2fit, ]
        self.__mainwidget.addTab(g2fit, "Fitting")
                                 
        # CONTIN tab
#        contintab = contin.MainContin()
#        self.__graphsWidgets += [contintab, ]
#        self.__mainwidget.addTab(contintab, "CONTIN")
        
        self.showMaximized()
        
        # Add docks
        self.__filedock = docks.FileDock()
        self.addDockWidget(qtc.Qt.LeftDockWidgetArea,self.__filedock)
        self.__filedock.onPlotRequest.connect(self.onPlotRequest)
        
    def closeEvent(self, evt):
        qtw.QApplication.instance().quit()

    def onPlotRequest(self, filelist):
        logger.debug(filelist)
        try:     
            self.__mainwidget.currentWidget().clear()
            self.__mainwidget.currentWidget().plot(filelist)
        except Exception as exc:
            logger.fatal(traceback.format_exc())
            qtw.QMessageBox.critical(self, "Error during plotting", str(exc))

            
            
    def exportDialog(self):
        """
        Launch the export dialog
        """
        
        files = self.__filedock.filesSelected
        
        if len(files) == 0:
            qtw.QMessageBox.critical(self, "Error", "No files selected for export.")
        else:        
            dial = XPCSExportDialog(files, self)
            dial.exec()
                
        