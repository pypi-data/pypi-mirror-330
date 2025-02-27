#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 15:46:18 2021

@author: opid02
"""

import h5py, hdf5plugin
import logging
import numpy as np
import pandas as pd
import os
from .result_file_old import XPCSResultFileOld

logger = logging.getLogger(__name__)

class NotXPCSFileException(Exception):
    pass


class XPCSResultFile(object):
    def __init__(self, filename):
        self.__filename = filename
        self._fd = None
    
    def __enter__(self):
        """
        Allow with statement
        """
        try:
            self._fd = XPCSResultFileNew(self.__filename)
        except NotXPCSFileException:
            pass
        
        if self._fd is None:
            self._fd = XPCSResultFileOld(self.__filename)
        
        return self._fd
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        self._fd = None
        return False



class XPCSResultFileNew(object):
    def __init__(self, filename):
        """
        Initialize the class with filename, open file
        """
        logger.debug("Open file %s",filename)
        self.__filename = filename
        self.__fd = None
        self.__fd = h5py.File(self.__filename, 'r', locking=False)
        
        self.__analysis_path = "/entry_0000/correlations/"
        self.__headers = None
        self.__aheaders = None
        
        self.checkFile()
        
    def __del__(self):
        """
        Take care of closing the file
        """
        if self.__fd is not None:
            self.close()
        
    def close(self):
        logger.debug("Closing file %s", self.__filename)
        self.__fd.close()
        self.__fd = None
        
        
    def checkFile(self):
        """
        Check magic string and version
        """
        if "MagicString" in self.__fd.attrs and self.__fd.attrs['MagicString'] == "XPCSResultFile_v2.0":
            return
        
        raise NotXPCSFileException("Unknown MagicString.")
            
            
    @property
    def headers(self):
        if type(self.__headers) != dict:
            self.__headers = dict()
            
            for k in self.__fd['/entry_0000/parameters'].keys():
                v = self.__fd['/entry_0000/parameters/%s'%k][()]
                
                if isinstance(v, bytes):
                    v = v.decode()
                
                self.__headers[k] = v
            
        return self.__headers
    
    @property
    def acq_headers(self):
        if type(self.__aheaders) != dict:
            self.__aheaders = dict()
            
            for k in self.__fd['/entry_0000/acquisition'].keys():
                v = self.__fd['/entry_0000/acquisition/%s'%k][()]
                
                if isinstance(v, bytes):
                    v = v.decode()
                
                self.__aheaders[k] = v
            
        return self.__aheaders
    
    @property
    def title(self):
        if 'title' in self.headers:
            return self.headers['title']
        
        return ""
    
    @property
    def timestamp(self):
        if 'timestamp' in self.acq_headers:
            return int(self.acq_headers['timestamp'])
        
        return None
        
            
    @property
    def filename(self):
        return os.path.basename(self.__filename)
            
    @property
    def saxs_curve_q(self):
        """
        q vector of SAXS 1D reduced curve
        """
        if not hasattr(self, '_XPCSResultFile__1D_average_q'):
            logger.debug("Load 1D saxs curve average")
            self.__1D_average_q = np.array(self.__fd.get('entry_0000/time_averaged/azimuthal_average/q'))
            
        return self.__1D_average_q
    
    @property
    def saxs_curve_Iq(self):
        """
        I(q) vector of SAXS 1D reduced curve
        """
        if not hasattr(self, '_XPCSResultFile__1D_average_Iq'):
            logger.debug("Load 1D saxs curve average")
            self.__1D_average_Iq = np.array(self.__fd.get('entry_0000/time_averaged/azimuthal_average/Intensity')).ravel()
            
        return self.__1D_average_Iq
    
    @property
    def default_2D_pattern(self):
        return "frame_average_norm"
    
    @property
    def available_2D_patterns(self):
        """
        Return the available 2D patterns keys, and the default one
        """
        R = []
        
        grp = self.__fd['/entry_0000/time_averaged']
        
        for f in grp:
            if isinstance(grp[f], h5py.Dataset) and len(grp[f].shape) == 2:
                R += [f,]
        
        return R
    
    def get_2D_pattern(self, key):
        """
        Return the corrected time averaged 2D pattern
        """
        # Cache is performed by h5py
        return np.array(self.__fd.get(f'entry_0000/time_averaged/{key}'))
    
    @property
    def available_2D_parameters(self):
        """
        Return the available 2D patterns keys, and the default one
        """
        R = []
        
        grp = self.__fd['/entry_0000/parameters']
        
        for f in grp:
            if isinstance(grp[f], h5py.Dataset) and len(grp[f].shape) == 2:
                R += [f,]
        
        return R
    
    
    def get_2D_parameter(self, key):
        """
        Return the corrected time averaged 2D pattern
        """
        # Cache is performed by h5py
        return np.array(self.__fd.get(f'entry_0000/parameters/{key}'))
    
    
    @property
    def analysis_keys(self):
        """
        Return the analysis keys, to be passed in analysis getter functions
        """
        return [ *self.__fd[self.__analysis_path].keys() ]
    
    
    def get_qmask(self, key):
        """
        Return the q-mask for specific analysis
        """

        roi_masks = np.array(self.__fd.get(f'entry_0000/correlations/{key}/roi_masks'))
        
        R = np.full(roi_masks.shape[1:], 0, dtype=np.uint8)
        
        for i in range(roi_masks.shape[0]):
            R[roi_masks[i,:,:]] = i+1
            
        return R
    
    def get_roi_masks(self, key):
        """
        Return the roi mask for specific analysis
        """

        return np.array(self.__fd.get(f'entry_0000/correlations/{key}/roi_masks'))
    
    def get_correlations(self, key):
        """
        Return lag, correlation function and standard deviation if any from specific analysis
        """
            
        lag = np.array(self.__fd.get(f'entry_0000/correlations/{key}/g2/lag'))
        cf  = np.array(self.__fd.get(f'entry_0000/correlations/{key}/g2/cf'))
        
        if f'entry_0000/correlations/{key}/g2/err' in self.__fd:
            std = np.array(self.__fd.get(f'entry_0000/correlations/{key}/g2/err'))
        else:
            std = None
            
        return (lag, cf, std)
    
    def get_q_values(self, key):
        """
        Return the q-values for the specific analysis
        """
        
        return np.array(self.__fd.get(f'entry_0000/correlations/{key}/parameters/q'))    
    
    def get_ttcf(self, key, index):
        """
        Return the actual q indexes used for this specific analysis
        """
        
        lag = np.array(self.__fd.get(f'entry_0000/correlations/{key}/twotime/lag'))
        age = np.array(self.__fd.get(f'entry_0000/correlations/{key}/twotime/age'))
        cf  = np.array(self.__fd[f'entry_0000/correlations/{key}/twotime/ttcf'][index,:,:])
            
        return cf, lag, age
    
    def get_ttcfs(self, key):
        """
        Return the ttcf 3D matrix
        """
        
        lag = np.array(self.__fd.get(f'entry_0000/correlations/{key}/twotime/lag'))
        age = np.array(self.__fd.get(f'entry_0000/correlations/{key}/twotime/age'))
        cf  = np.array(self.__fd[f'entry_0000/correlations/{key}/twotime/ttcf'])
            
        return cf, lag, age
        

