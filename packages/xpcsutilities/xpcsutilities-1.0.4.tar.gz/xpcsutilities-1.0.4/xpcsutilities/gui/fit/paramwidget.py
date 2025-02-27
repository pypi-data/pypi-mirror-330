# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtWidgets as qtw

import numpy as np

import logging
logger = logging.getLogger(__name__)

class paramwidget(qtw.QWidget, object):
    def __init__(self):
        super().__init__()
        
        self.__layout = qtw.QGridLayout()
        self.__layout.setColumnStretch(0,1)
        self.__layout.setColumnStretch(1,2)
        self.__layout.setColumnStretch(2,1)
        self.__layout.setColumnStretch(3,2)
        self.__layout.setColumnMinimumWidth(1,100)
        self.__layout.setColumnMinimumWidth(3,100)
        self.setLayout(self.__layout)
        
        self.__value = qtw.QLineEdit()
        self.__mvalue = qtw.QLineEdit()        
        self.__Mvalue = qtw.QLineEdit()
        
        self.__isFixedValue = qtw.QCheckBox()
        self.__isFixedValue.setChecked(False)
        
        self.__isMultipleValue = qtw.QCheckBox()
        self.__isMultipleValue.setChecked(True)
        
        self.__layout.addWidget(qtw.QLabel("Initial: "),0,0)
        self.__layout.addWidget(self.__value,0,1)
        
        self.__layout.addWidget(qtw.QLabel("Fixed: "),0,2)
        self.__layout.addWidget(self.__isFixedValue,0,3)
        
        self.__layout.addWidget(qtw.QLabel("Minimum: "),1,0)
        self.__layout.addWidget(self.__mvalue,1,1)
        
        self.__layout.addWidget(qtw.QLabel("Maximum: "),1,2)
        self.__layout.addWidget(self.__Mvalue,1,3)
        
        self.__layout.addWidget(qtw.QLabel("One value per curve: "),2,0,1,3)
        self.__layout.addWidget(self.__isMultipleValue,2,3)
        
        self.setValue(0.)
        self.setMinval(0.)
        self.setMaxval(+np.inf)
    
    def value(self):
        return float(self.__value.text())
    
    def setValue(self, val : float):
        self.__value.setText('%.5e'%val)
        
    def minval(self):
        return float(self.__mvalue.text())
    
    def setMinval(self, mval : float):
        self.__mvalue.setText('%.5e'%mval)
        
    def maxval(self):
        return float(self.__Mvalue.text())
    
    def setMaxval(self, mval : float):
        self.__Mvalue.setText('%.5e'%mval)
    
    def isFixed(self):
        return self.__isFixedValue.isChecked()
    
    def setIsFixed(self, fix : bool):
        self.__isFixedValue.setChecked(fix)
        
    def isMultipleValue(self):
        return self.__isMultipleValue.isChecked()
    
    def setIsMultipleValue(self, mul : bool):
        self.__isMultipleValue.setChecked(mul)