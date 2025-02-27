# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as qtw
import numpy as np

class ParamsTable(qtw.QWidget):
    def __init__(self):
        super().__init__()
        
        self.__defaultValues = dict()
        
        self.__defaultValues['beta'] = dict()
        self.__defaultValues['beta']['init'] = .5
        self.__defaultValues['beta']['scale'] = 1
        self.__defaultValues['beta']['min'] = 0
        self.__defaultValues['beta']['max'] = 1
        self.__defaultValues['beta']['fixed'] = False
        self.__defaultValues['beta']['scaled'] = False
        self.__defaultValues['beta']['qdep'] = True
        
        self.__defaultValues['D'] = dict()
        self.__defaultValues['D']['init'] = 1e6
        self.__defaultValues['D']['scale'] = 1e6
        self.__defaultValues['D']['min'] = 0
        self.__defaultValues['D']['max'] = np.inf
        self.__defaultValues['D']['fixed'] = False
        self.__defaultValues['D']['scaled'] = False
        self.__defaultValues['D']['qdep'] = False
        
        self.__defaultValues['v'] = dict()
        self.__defaultValues['v']['init'] = 6e4
        self.__defaultValues['v']['scale'] = 1e4
        self.__defaultValues['v']['min'] = 0
        self.__defaultValues['v']['max'] = np.inf
        self.__defaultValues['v']['fixed'] = False
        self.__defaultValues['v']['scaled'] = False
        self.__defaultValues['v']['qdep'] = False
        
        self.__defaultValues['alpha'] = dict()
        self.__defaultValues['alpha']['init'] = .5
        self.__defaultValues['alpha']['scale'] = .1
        self.__defaultValues['alpha']['min'] = 0
        self.__defaultValues['alpha']['max'] = 1
        self.__defaultValues['alpha']['fixed'] = False
        self.__defaultValues['alpha']['scaled'] = False
        self.__defaultValues['alpha']['qdep'] = False
        
        self.__defaultValues['Gamma'] = dict()
        self.__defaultValues['Gamma']['init'] = 50
        self.__defaultValues['Gamma']['scale'] = 1e1
        self.__defaultValues['Gamma']['min'] = 0
        self.__defaultValues['Gamma']['max'] = np.inf
        self.__defaultValues['Gamma']['fixed'] = False
        self.__defaultValues['Gamma']['scaled'] = False
        self.__defaultValues['Gamma']['qdep'] = True
        
        self.__defaultValues['n'] = dict()
        self.__defaultValues['n']['init'] = 1
        self.__defaultValues['n']['scale'] = 1
        self.__defaultValues['n']['min'] = 1
        self.__defaultValues['n']['max'] = 2
        self.__defaultValues['n']['fixed'] = False
        self.__defaultValues['n']['scaled'] = False
        self.__defaultValues['n']['qdep'] = False
        
        self.__defaultValues['T'] = dict()
        self.__defaultValues['T']['init'] = 295.15
        self.__defaultValues['T']['scale'] = 1
        self.__defaultValues['T']['min'] = 0
        self.__defaultValues['T']['max'] = np.inf
        self.__defaultValues['T']['fixed'] = True
        self.__defaultValues['T']['scaled'] = False
        self.__defaultValues['T']['qdep'] = False
        
        self.__defaultValues['eta'] = dict()
        self.__defaultValues['eta']['init'] = .954e-3
        self.__defaultValues['eta']['scale'] = 1e-3
        self.__defaultValues['eta']['min'] = 0
        self.__defaultValues['eta']['max'] = np.inf
        self.__defaultValues['eta']['fixed'] = True
        self.__defaultValues['eta']['scaled'] = False
        self.__defaultValues['eta']['qdep'] = False
        
        self.__defaultValues['r'] = dict()
        self.__defaultValues['r']['init'] = 80e-9
        self.__defaultValues['r']['scale'] = 1e-9
        self.__defaultValues['r']['min'] = 0
        self.__defaultValues['r']['max'] = np.inf
        self.__defaultValues['r']['fixed'] = False
        self.__defaultValues['r']['scaled'] = False
        self.__defaultValues['r']['qdep'] = False
        
        self.__layout = qtw.QVBoxLayout()
        self.setLayout(self.__layout)
        
        self.__maintable = qtw.QTableWidget()
        self.__layout.addWidget(self.__maintable)
        
        self.__maintable.setColumnCount(1)
        self.__maintable.setRowCount(7)
        
        self.__titles = dict()
        self.__titles['initv'] = 'Initial'
        self.__titles['maxv'] = 'Maximum'
        self.__titles['minv'] = 'Minimum'
        self.__titles['fixed'] = 'Fixed'
        self.__titles['scaled'] = 'Scaled'
        self.__titles['scale'] = 'Scale'
        self.__titles['qdep'] = 'q-dep'
        
        for r,t in enumerate(self.__titles.values()):
            self.__maintable.setItem(r,0,qtw.QTableWidgetItem(t))
            
        self.__maintable.setColumnWidth(0, 80)
        self.__usedVariables = dict()
        
    def showVariables(self, lstv):
        
        for i in range(len(self.__usedVariables)):
            self.__maintable.hideColumn(i+1)
        
        for v in lstv:
            if v in self.__usedVariables:
                self.__maintable.showColumn(self.__usedVariables[v]['colid'])
            else:
                vard = dict()
                idc = self.__maintable.columnCount()
                self.__maintable.setColumnCount(idc+1)
                
                vard['colid'] = idc
                
                vard['initv'] = qtw.QLineEdit()
                vard['maxv'] = qtw.QLineEdit()
                vard['minv'] = qtw.QLineEdit()
                vard['fixed'] = qtw.QCheckBox()
                vard['scaled'] = qtw.QCheckBox()
                vard['scale'] = qtw.QLineEdit()
                vard['qdep'] = qtw.QCheckBox()
                
                for r,k in enumerate(self.__titles.keys()):
                    self.__maintable.setCellWidget(r,idc, vard[k])
                    
                self.__usedVariables[v] = vard
                self.__maintable.setColumnWidth(idc, 80)
                
                if v in self.__defaultValues:
                    dv = self.__defaultValues[v]
                    vard['initv'].setText('%.2e'%dv['init'])
                    vard['maxv'].setText('%.2e'%dv['max'])
                    vard['minv'].setText('%.2e'%dv['min'])
                    vard['scale'].setText('%.2e'%dv['scale'])
                    vard['scaled'].setChecked(dv['scaled'])
                    vard['fixed'].setChecked(dv['fixed'])
                    vard['qdep'].setChecked(dv['qdep'])
                else:
                    vard['initv'].setText('1.')
                    vard['maxv'].setText('inf')
                    vard['minv'].setText('0')
                    vard['scale'].setText('1')
                    vard['scaled'].setChecked(False)
                    vard['fixed'].setChecked(False)
                    vard['qdep'].setChecked(True)
                    
                    
        self.__maintable.setHorizontalHeaderLabels(['', *self.__usedVariables.keys()])
        
    def getVariables(self):
        
        ret = dict()
        
        for k,it in self.__usedVariables.items():
            if not self.__maintable.isColumnHidden(it['colid']):

                v = dict()
                v['value'] = float(it['initv'].text())
                v['min']  = float(it['minv'].text())
                v['max']  = float(it['maxv'].text())
                v['scale'] = float(it['scale'].text())
                
                v['isFixed'] = it['fixed'].isChecked()
                v['isScaled'] = it['scaled'].isChecked()
                v['isMultiple'] = it['qdep'].isChecked()
                
                ret[k] = v
                
        return ret
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                