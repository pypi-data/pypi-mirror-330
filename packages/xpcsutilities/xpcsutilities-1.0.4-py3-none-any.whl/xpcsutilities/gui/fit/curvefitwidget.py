# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Qt5Agg')

import PyQt5.QtWidgets as qtw

import numpy as np
import logging
logger = logging.getLogger(__name__)

#from .paramwidget import paramwidget
from .parametertable import ParamsTable

class CurveFitWidget(qtw.QGroupBox):
    def __init__(self):
        super().__init__("Curve fitting")
        
        self.__curve_fit_layout = qtw.QFormLayout()
        self.setLayout(self.__curve_fit_layout)
        
        self.__fit_max_lag = qtw.QDoubleSpinBox()
        self.__fit_max_lag.setDecimals(6)
        self.__fit_max_lag.setValue(0)
        self.__fit_max_lag.setMaximum(np.inf)
        self.__curve_fit_layout.addRow("Maximum lag time (0: deactivated)", self.__fit_max_lag)
        
        self.__g1_library = dict()
        self.__g1_library['dif'] = {'Name': 'Diffusive', 'Fun': 'exp(-D*t*q^2)', 'g1': lambda t,q,D,**kwargs : np.exp(-D*t*q**2) }
        self.__g1_library['difr'] = {'Name': 'Diffusive (radius)', 'Fun': 'exp(-kB*T*t*q^2/(6*pi*eta*r))', 'g1': lambda t,q,T,eta,r,**kwargs : np.exp(-1.380e-23*T*t*(q*1e9)**2/(6*np.pi*eta*r)) }
        self.__g1_library['exp'] = {'Name': 'Exponential', 'Fun': ' exp(-Gamma*t)', 'g1': lambda t,q,Gamma,**kwargs : np.exp(-Gamma*t) }
        self.__g1_library['stexp'] = {'Name': 'Stretched Exponential', 'Fun': ' exp(-Gamma*t^n)', 'g1': lambda t,q,Gamma,n,**kwargs : np.exp(-Gamma*t**n) }
        self.__g1_library['conv'] = {'Name': 'Convection', 'Fun': ' 1 + alpha*(sinc(t*q*v)-1)', 'g1': lambda t,q,v,alpha,**kwargs : 1.+alpha*(np.sinc(t*q*v/np.pi)-1.) }
        
        self.__curve_fit_layout.addRow(qtw.QLabel("Select g_1 to fit curves"))    
        
        for k,g1 in self.__g1_library.items():
            chkb = qtw.QCheckBox()
            chkb.stateChanged.connect(self.__displayFitParameters)
            
            g1['chkb'] = chkb
            self.__curve_fit_layout.addRow('%s %s'%(g1['Name'], g1['Fun']), g1['chkb'])
            
        self.__paramsTable = ParamsTable()
        self.__curve_fit_layout.addRow(self.__paramsTable)
            
        #self.__params_fit_layout = qtw.QFormLayout()
        #self.__curve_fit_layout.addRow(self.__params_fit_layout)
            
        # Fitting parameters
#        self.__g1_params = dict()
#        for k, g1 in self.__g1_library.items():
#            for p in g1['g1'].__code__.co_varnames:
#                if p not in self.__g1_params and p not in ('t','q','kwargs'):
#                    self.__g1_params[p] = {'name':p, 'widget': None }
        
        self.__fitContrast = False
          
    def setFitContrast(self, fit):
        self.__fitContrast = fit
        self.__displayFitParameters()
        
    def getFitContrast(self):
        return self.__fitContrast
        
    def __displayFitParameters(self):
        params = ['beta'] if self.__fitContrast else [] 
        for k, g1 in self.__g1_library.items():
            if g1['chkb'].isChecked():
                for p in g1['g1'].__code__.co_varnames:
                    if p not in params and p not in ('t','q','kwargs'):
                        params += [p,]
                        
        self.__paramsTable.showVariables(params)
                        
#        for n,p in self.__g1_params.items():
#            if n not in params:
#                if p['widget'] is not None:
#                    self.__params_fit_layout.removeRow(p['widget'])
#                    p['widget'] = None
#            elif p['widget'] is None:
#                p['widget'] = paramwidget()
#                label = qtw.QLabel(p['name'])
#                label.setStyleSheet("font-weight: bold; color: blue");
#                self.__params_fit_layout.addRow(label,p['widget'])
                
                
    def strModel(self):
        m = ''
        for k, g1 in self.__g1_library.items():
            if g1['chkb'].isChecked():
                m += '(%s)'%g1['Fun']
        return m
    
    def maxlag(self):
        val = self.__fit_max_lag.value()
        return val if val > 0 else +np.inf

    def fitfunction(self):
        """
        Return the fitting functions and copy of internal parameters dict
        """
        
        fncs = []
        for k, g1 in self.__g1_library.items():
            if g1['chkb'].isChecked():                
                fncs += [g1['g1'],]
                
        # Get parameters options
        parval = self.__paramsTable.getVariables()
        
        # This function will be passed to curve_fit, take arbitrary number of parameters to fit, return the cf matrix
        def fnc(t,q,*args, scale=True, sepf=False):
            q = q.ravel()
            N = q.shape[0]
            
            ret = np.ones((t.shape[0], N), dtype=np.float32)
            ret2 = np.ones((t.shape[0], N*len(fncs)), dtype=np.float32)
            pars = self.args2params(N,parval,*args, scale=scale) # Rebuild parameters for each curve
                    
            for i in range(N):
                for j, fn in enumerate(fncs):
                    res = fn(t,q[i],**{k:v[i] for k,v in pars.items()}) # Unpack parameters from arrays
                    ret[:,i] *= res**2
                    ret2[:,i*len(fncs)+j] = res**2
                    
                if 'beta' in pars:
                    ret[:,i] = ret[:,i]*pars['beta'][i]
                    
            return ret if not sepf else (ret, ret2, len(fncs))
            
        return fnc, parval.copy()
    
    def initValues(self, N : int, *, scale=True):
        """
        Return the initial values array to be passed to fitting function.
        """
        
        vals = []
#        for k,p in self.__g1_params.items():
#            scale = scales[k] if k in scales and scales[k] > 0. else 1.
#            if p['widget'] is not None and not p['widget'].isFixed():
#                val = p['widget'].value()/scale
#                vals += [val,]*N if p['widget'].isMultipleValue() else [val,]
        
        for k,v in self.__paramsTable.getVariables().items():
            if v['isFixed']:
                vals += [v['value'],]
            else:
                scale = 1.
                if scale and v['isScaled']:
                    if v['scale'] != 0.:
                        scale = v['scale']
                    else:
                        logger.warning("Scale is 0 for variable %s. Scaling disabled for this variable."%k)
                        
                val = v['value']/scale
                vals += [val,]*N if v['isMultiple'] else [val,]
                    
        return np.array(vals)
    
    def bounds(self, N : int, *, scale=True):
        """
        Return the lower and upper bounds to be passed to fitting function.
        """
        
        ma,Ma = [],[]
#        if scales is None:
#            scales = dict()
#            
#        for k,p in self.__g1_params.items():
#            scale = scales[k] if k in scales and scales[k] > 0. else 1.
#            if p['widget'] is not None and not p['widget'].isFixed():
#                m += [p['widget'].minval()/scale,]*N if p['widget'].isMultipleValue() else [p['widget'].minval()/scale,]
#                M += [p['widget'].maxval()/scale if p['widget'].maxval() != 0 else +np.inf,]*N if p['widget'].isMultipleValue() else [p['widget'].maxval()/scale if p['widget'].maxval() != 0 else +np.inf,]
        
        for k,v in self.__paramsTable.getVariables().items():
            if v['isFixed']:
                if v['value'] > 0:
                    ma += [v['value']*0.999,]
                    Ma += [v['value']*1.001,]
                elif v['value'] < 0:
                    ma += [v['value']*1.001,]
                    Ma += [v['value']*.999,]
                else:
                    ma += [-.0001,]
                    Ma += [.0001,]
            else:
                scale = 1.
                if scale and v['isScaled']:
                    if v['scale'] != 0.:
                        scale = v['scale']
                    else:
                        logger.warning("Scale is 0 for variable %s. Scaling disabled for this variable."%k)
                        
                m = v['min']/scale
                ma += [m,]*N if v['isMultiple'] else [m,]
                
                M = v['max']/scale
                Ma += [M,]*N if v['isMultiple'] else [M,]
        
        return np.array(ma), np.array(Ma)
    
    def args2params(self, N, parval, *args, scale=True):
        """
        Convert the array of parameters to parameters dictionary containing arrays of values
        """
#        
#        if scales is None:
#            scales = dict()
#        
#        if parval is None:
#            params = []
#            fncs = []
#            for k, g1 in self.__g1_library.items():
#                if g1['chkb'].isChecked():
#                    for p in g1['g1'].__code__.co_varnames:
#                        if p not in params and p not in ('q','t','kwargs'):
#                            params += [p,]
#                    
#                    fncs += [g1['g1'],]
#        
#            parval = dict()
#            for k,p in self.__g1_params.items():
#                if k in params: # Should be instanciated if in params
#                    parval[k] = { 'value': p['widget'].value(),
#                                  'isFixed': p['widget'].isFixed(),
#                                  'isMultiple': p['widget'].isMultipleValue() }
        
        pars=dict()
        i=0
        
        for k,p in parval.items():
            factor = p['scale'] if scale and p['isScaled'] and p['scale'] != 0 else 1.
            if p['isFixed']:
                pars[k] = np.array([p['value'],]*N).ravel()
                i += 1
            elif p['isMultiple']:
                pars[k] = np.array([a*factor for a in args[i:i+N]]).ravel()
                i += N
            else:
                pars[k] = np.array([args[i]*factor,]*N).ravel()
                i += 1
                
        return pars



