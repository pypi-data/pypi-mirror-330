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

from xpcsutilities.tools import contin
from . import tab_res_contin


class MainContin(qtw.QWidget):
    """
    Contains the main tab for CONTIN analysis
    """
    
    def __init__(self):
        """
        Widget initialization
        """
        
        super().__init__()
        
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        self.__main = qtw.QSplitter()
        self.__layout.addWidget(self.__main)
        
        self.__mainsettings = qtw.QWidget()
        self.__mainsettings.setMaximumWidth(500)
        self.__mainsettingslayout = qtw.QVBoxLayout()
        self.__mainsettings.setLayout(self.__mainsettingslayout)
        self.__main.addWidget(self.__mainsettings)
        
        self.__grp1settings = qtw.QGroupBox("CONTIN settings")
        self.__grp1settingslayout = qtw.QFormLayout()
        self.__grp1settings.setLayout(self.__grp1settingslayout)
        self.__mainsettingslayout.addWidget(self.__grp1settings)
        
        self.__mintime = qtw.QLineEdit()
        self.__mintime.setText("0")
        self.__grp1settingslayout.addRow("Minimum of Laplace variable (0 for auto)", self.__mintime)
        
        self.__maxtime = qtw.QLineEdit()
        self.__maxtime.setText("0")
        self.__grp1settingslayout.addRow("Maximum of Laplace variable (0 for auto)", self.__maxtime)
        
        self.__Ndistrib = qtw.QSpinBox()
        self.__Ndistrib.setMinimum(1)
        self.__Ndistrib.setMaximum(100)
        self.__Ndistrib.setValue(20)
        self.__grp1settingslayout.addRow("Number of Laplace points", self.__Ndistrib)
        
        # Progress bar
        self.__grpprgbar = qtw.QGroupBox()
        self.__mainsettingslayout.addWidget(self.__grpprgbar)
        self.__prgbarlayout = qtw.QFormLayout()
        self.__grpprgbar.setLayout(self.__prgbarlayout)
        
        self.__fileprocessbar = qtw.QProgressBar()
        self.__qprocessbar = qtw.QProgressBar()
        self.__prgbarlayout.addRow("Files: ", self.__fileprocessbar)
        self.__prgbarlayout.addRow("q: ", self.__qprocessbar)

        # Results tabs
        self.__restab = qtw.QTabWidget()
        self.__main.addWidget(self.__restab)

        
    def clear(self):
        """
        Used to remotely clean the tab. Ignored here.
        """
        pass
    
    def plot(self, filelist):
        """
        Start the analysis
        """
        mins = float(self.__mintime.text())
        maxs = float(self.__maxtime.text())
        
        self.__fileprocessbar.setMaximum(len(filelist))
        self.__fileprocessbar.setMinimum(0)
        self.__fileprocessbar.setValue(0)
        
        for j, fn in enumerate(filelist):
            with XPCSResultFile(fn) as fd:
                for k in fd.analysis_keys:
                    qs = fd.get_q_values(k)
                    tau, cf, std = fd.get_correlations(k)
                    
                    self.__qprocessbar.setMaximum(len(qs))
                    self.__qprocessbar.setMinimum(0)
                    self.__qprocessbar.setValue(0)
                    
                    
                    if mins == 0:
                        min_s = np.min(tau)
                    else:
                        min_s = mins
                        
                    if maxs == 0:
                        max_s = np.max(tau)
                    else:
                        max_s = maxs
        
                    s = np.logspace(np.log10(min_s), np.log10(max_s), self.__Ndistrib.value())
                    
                    beta = qs*0
                    G = np.zeros((len(s), len(qs)))
                    
                    for i, q in enumerate(qs):
                        beta[i], G[:,i] = contin.contin(tau, cf[:,i]-1, s)
                        self.__qprocessbar.setValue(i+1)
                        
                    restab = tab_res_contin.ContinResult()
                    self.__restab.addTab(restab, f"{fn} {k}")
                    restab.plot(qs, tau, cf, s, beta, G)
                    
            self.__fileprocessbar.setValue(j+1)
        
        
