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

logger = logging.getLogger(__name__)


class XPCSResultFileOld(object):
    def __init__(self, filename):
        """
        Initialize the class with filename, open file
        """
        logger.debug("Open file %s",filename)
        self.__filename = filename
        self.__fd = None
        self.__fd = h5py.File(self.__filename, 'r', locking=False)
        
        self.__analysis_path = "/entry_0000/dynamix/correlations/directions/"
        self.__analysis_basepath = self.__analysis_path+"/%s"

        self.__headers = None
        
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
        
        
    def checkFile(self):
        """
        Check magic string and version
        """
        from .result_file import NotXPCSFileException
        if "entry_0000/title" in self.__fd and "version" in self.__fd["entry_0000"].attrs:
            self.__version = self.__fd['entry_0000'].attrs['version']
            if self.__fd.get('entry_0000/title')[0].decode('utf-8') != "XPCSResultFile":
                raise NotXPCSFileException("Invalid title. Should be XPCSResultFile, not %s"%self.__fd.get('entry_0000/title')[0].decode('utf-8'))
                
            logger.debug("File version: %s", self.__version)
        else:
            raise NotXPCSFileException("Can't find filetype or version for given file.")
            

            
    @property
    def headers(self):
        if type(self.__headers) != dict:
            self.__headers = dict()
            
            for k in self.__fd['/entry_0000/configuration'].keys():
                v = self.__fd['/entry_0000/configuration/%s'%k][()]
                
                if isinstance(v, bytes):
                    v = v.decode()
                
                self.__headers[k] = v
            
        return self.__headers
    
    @property
    def acq_headers(self):
        return {}
    
    @property
    def title(self):
        if 'title' in self.headers:
            return self.headers['title']
        
        return ""
    
    @property
    def timestamp(self):
        if 'timestamp' in self.__fd['/entry_0000/']:
            return self.__fd['/entry_0000/timestamp'][()]
        
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
            self.__1D_average_q = np.array(self.__fd.get('entry_0000/dynamix/time_averaged/1D/q'))
            
        return self.__1D_average_q
    
    @property
    def saxs_curve_Iq(self):
        """
        I(q) vector of SAXS 1D reduced curve
        """
        if not hasattr(self, '_XPCSResultFile__1D_average_Iq'):
            logger.debug("Load 1D saxs curve average")
            self.__1D_average_Iq = np.array(self.__fd.get('entry_0000/dynamix/time_averaged/1D/Iq')).ravel()
            
        return self.__1D_average_Iq
    
    @property
    def default_2D_pattern(self):
        return "corrected"
    
    @property
    def available_2D_patterns(self):
        """
        Return the available 2D patterns keys, and the default one
        """
        R = []
        
        grp = self.__fd['/entry_0000/dynamix/time_averaged']
        
        for f in grp:
            if isinstance(grp[f], h5py.Dataset) and len(grp[f].shape) == 2:
                R += [f,]
        
        return R
        
    
    def get_2D_pattern(self, key):
        """
        Return the corrected time averaged 2D pattern
        """
        # Cache is performed by h5py
        return np.array(self.__fd.get(f'entry_0000/dynamix/time_averaged/{key}'))
    
    @property
    def available_2D_parameters(self):
        """
        Return the available 2D patterns keys, and the default one
        """
        R = []
        
        grp = self.__fd['/entry_0000/dynamix/parameters']
        
        for f in grp:
            if isinstance(grp[f], h5py.Dataset) and len(grp[f].shape) == 2:
                R += [f,]
        
        return R
    
    def get_2D_parameter(self, key):
        """
        Return the corrected time averaged 2D pattern
        """
        # Cache is performed by h5py
        return np.array(self.__fd.get(f'entry_0000/dynamix/parameters/{key}'))
    
    
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

        fkey = self.__analysis_basepath%key
        
        if fkey not in self.__fd:
            raise ValueError("Unknown analysis %s"%(key))

        return np.array(self.__fd.get('%s/qmask'%fkey))

    
    def get_roi_masks(self, key):
        """
        Return the roi mask for specific analysis
        """

        qm = self.get_qmask(key)
        M = int(np.nanmax(qm))
        
        roi_masks = np.empty((M-1, *qm.shape), dtype=np.bool)
        
        for i in range(M-1):
            roi_masks[i,:,:] = qm == i+1

        return roi_masks
    
    def get_correlations(self, key):
        """
        Return lag, correlation function and standard deviation if any from specific analysis
        """
        fkey = self.__analysis_basepath%key
        
        if fkey not in self.__fd:
            raise ValueError("Unknown analysis %s"%(key))
            
        ts = np.array(self.__fd.get('%s/correlation/timeshift'%fkey))
        
        if len(ts.shape) == 0:
            ts = np.array(self.__fd.get('%s/correlation/lag'%fkey))
        
        cf = np.array(self.__fd.get('%s/correlation/cf'%fkey))
        
        if '%s/correlation/std'%fkey in self.__fd:
            std = np.array(self.__fd.get('%s/correlation/std'%fkey))
        else:
            std = None
            
        return (ts.ravel(), cf.T, std.T)
    
    def _get_q_index(self, key):
        """
        Return the actual q indexes used for this specific analysis
        """
        fkey = self.__analysis_basepath%key
        
        if fkey not in self.__fd:
            raise ValueError("Unknown analysis %s"%(key))
            
        return np.array(self.__fd.get('%s/q_index'%fkey), dtype=np.int32)
    
    def get_q_values(self, key):
        """
        Return the q-values for the specific analysis
        """
        
        qidx = self._get_q_index(key)
        rng  = np.array(self.__fd.get('entry_0000/dynamix/correlations/q_index_min_max'))
        
        msk = np.isin(rng[:,0], qidx)
        
        return (rng[msk,1] + rng[msk,2])/2.
    
    def get_ttcf(self, key, index):
        """
        Return the actual q indexes used for this specific analysis
        """
        fkey = self.__analysis_basepath%key
        
        if fkey not in self.__fd:
            raise ValueError("Unknown analysis %s"%(key))
            
        ttcf_ds = self.__fd['%s/2times_correlation/ttcf'%fkey]
        
        if index < 1 or index > ttcf_ds.shape[0]:
            raise ValueError(f"Invalid index {index} {ttcf_ds.shape}")
            
        age = np.array(self.__fd.get('%s/2times_correlation/age'%fkey))
        timeshift = np.array(self.__fd.get('%s/2times_correlation/timeshift'%fkey))
        
        if len(timeshift.shape) == 0:
            timeshift = np.array(self.__fd.get('%s/2times_correlation/lag'%fkey))
        
        return (np.array(ttcf_ds[index-1,:,:], dtype=ttcf_ds.dtype), timeshift.ravel(), age.ravel())
    
    def get_ttcfs(self, key):
        """
        Return the ttcf 3D matrix
        """
        fkey = self.__analysis_basepath%key
        
        if fkey not in self.__fd:
            raise ValueError("Unknown analysis %s"%(key))
            
        ttcf_ds = self.__fd['%s/2times_correlation/ttcf'%fkey]
            
        age = np.array(self.__fd.get('%s/2times_correlation/age'%fkey))
        timeshift = np.array(self.__fd.get('%s/2times_correlation/timeshift'%fkey))
        
        if len(timeshift.shape) == 0:
            timeshift = np.array(self.__fd.get('%s/2times_correlation/lag'%fkey))
            
        return (np.array(ttcf_ds, dtype=ttcf_ds.dtype), timeshift.ravel(), age.ravel())

        

