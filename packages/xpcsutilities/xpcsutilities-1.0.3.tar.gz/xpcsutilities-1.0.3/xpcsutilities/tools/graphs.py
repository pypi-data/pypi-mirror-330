#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 18:32:25 2021

@author: opid02
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import logging
import numpy as np
from .result_file import XPCSResultFile
import scipy.optimize as opt

#plt.rcParams.update({
#    "text.usetex": False,
#    "font.family": "sans-serif",
#    "font.sans-serif": ["Helvetica"]})

logger = logging.getLogger(__name__)

def qindex_colors(qidx, colormap='default'):
    
    if colormap == 'default':
        cmap = mpl.cm.terrain
        maxval = np.max(qidx)/.76
        norm = mpl.colors.Normalize(vmin=np.min(qidx), vmax=maxval)
        
        cmap, norm = truncate_colormap(cmap, norm)
        return (cmap, norm, maxval)
    else:
        cmap = plt.get_cmap(colormap)
        maxval = np.max(qidx)
        norm = mpl.colors.Normalize(vmin=np.min(qidx), vmax=maxval)
        return (cmap, norm, maxval)
    
def symbol(i):
    sym = ['o', 's', '^', 'v', '>', '<', 'd']
    
    sid = i%len(sym)
    return sym[sid]
        
def truncate_colormap(cmap, norm, minval=0.0, maxval=0.76, n=100):
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    norm2 = mpl.colors.Normalize(vmin=norm.vmin, vmax=norm.vmax*maxval)
    return new_cmap, norm2

def plot_SAXS_with_qranges(file):
    ax = plt.subplot(111)
    ax.plot(file.saxs_curve[:,0], file.saxs_curve[:,1])
    
    (cmapi, normi, mv) = qindex_colors(file.q_ranges[:,0])
    
    for i,qi in enumerate(file.q_ranges[:,0]):
        ax.fill_between(file.saxs_curve[:,0], file.saxs_curve[:,1], where=np.logical_and(file.saxs_curve[:,0] >= file.q_ranges[i,1], file.saxs_curve[:,0] <= file.q_ranges[i,2]), color=cmapi(normi(qi)))
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$q (nm^-1)$')
    ax.set_ylabel('$I(q)$')
    
def plot_analysis_qranges(file, eta=0.89e-23, T=298, exp=1.):
    
    fig = plt.gcf()
    gs = fig.add_gridspec(3,len(file.analysis_keys)*2+1,width_ratios=[*[30/len(file.analysis_keys)]*(2*len(file.analysis_keys)), 1])
    
    ax = None
    
    # SAXS pattern colormap
    patt = file.saxs_pattern
    
    cmap = mpl.cm.jet
    norm = mpl.colors.LogNorm()
    
    # qmask colorbar
    q_ranges = file.q_ranges
    qs = (q_ranges[:,1]+q_ranges[:,2])/2.
    (cmapi, normi, mv) = qindex_colors(q_ranges[:,0])
    
    # Hydraulic radius
    kB = 1.38e-23
    def Rh(k):
        return (kB*T)/(6.*np.pi*eta*k)
    
    # fit functions
    def model(t,beta,D, sf):
        return 1. + beta*np.exp(-2.*D*t**sf)
    
    def propmodel(q,k):
        return k*q
    
    def sqmodel(q,k):
        return k*q**2
    
    bnd_st = (1.,0, +np.inf)
    
    if exp is not None:
        bnd_st = [exp,exp, exp+0.00001]
    
    for i,k in enumerate(file.analysis_keys):
        if ax is None:
            ax1 = fig.add_subplot(gs[0,i*2:i*2+2])
            ax = ax1
            #cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap, norm=norm)
        else:
            ax1 = fig.add_subplot(gs[0,i*2:i*2+2], sharex=ax, sharey=ax)            
        
        ax1.imshow(patt, cmap=cmap, norm=norm)
        qmask = np.array(file.get_qmask(k), np.float32)
        qmask[qmask == 0] = np.nan
        qmask[file.mask == 0] = mv
        ax1.imshow(qmask, cmap=cmapi, norm=normi, alpha=.6)
        
        (ts, cf, std) = file.get_correlations(k)
        kk = np.zeros((cf.shape[1],3))
        
        ax2 = fig.add_subplot(gs[1,i*2:i*2+2])
        for ii,qi in enumerate(file.get_q_index(k)):
            ax2.plot(ts, cf[:,ii], ".", color=cmapi(normi(qi)))
            
            msk = np.isnan(cf[:,ii]) == False
            
            k0 = opt.curve_fit(model, ts[msk].ravel(),cf[msk,ii], [0.3,1e2,bnd_st[0]], bounds=([0,0,bnd_st[1]],[1,+np.inf,bnd_st[2]]))
            ax2.plot(ts, model(ts,*k0[0]), ':', color=cmapi(normi(qi)))
            kk[ii,:] = k0[0]
            
        ax2.set_xscale('log')
        
        ax3 = fig.add_subplot(gs[2,i*2])
        ax4 = fig.add_subplot(gs[2,i*2+1])
        
        qq = np.array([qs[i-1] for i in file.get_q_index(k)])
        ax3.plot(qq, kk[:,0], 'o')
        ax4.plot(qq, kk[:,1], 'o')
        
        klog = np.polyfit(np.log(qq),np.log(kk[:,1]),1)
        klin = opt.curve_fit(propmodel, qq, kk[:,1], np.mean(kk[:,1]/qq))
        ksq  = opt.curve_fit(sqmodel, qq, kk[:,1], np.mean(kk[:,1]/qq**2))
        
        gamma_log = np.exp(np.polyval(klog,np.log(qq)))
        gamma_lin = propmodel(qq, klin[0][0])
        gamma_sq  = sqmodel(qq, ksq[0][0])
        
        r2 = lambda g: 1.-np.sum((kk[:,1]-g)**2)/np.sum((kk[:,1]-np.mean(kk[:,1]))**2)
        
        ax4.plot(qq,gamma_log, label='$%.03eq^{%.02f}, r^2=%.3f$'%(np.exp(klog[1]),klog[0], r2(gamma_log)))
        ax4.plot(qq,gamma_lin, label='$%.03eq, r^2=%.3f$'%(klin[0][0], r2(gamma_lin)))
        ax4.plot(qq,gamma_sq , label='$%.03eq^2, Rh=%.1f~nm$, r^2=%.3f'%(ksq[0][0],1e9*Rh(ksq[0][0]), r2(gamma_sq)))
        ax4.legend()
        
        ax4.set_xscale('log'); ax4.set_yscale('log')
        
        ax2.set_xlabel('$ts (s)$'); ax2.set_ylabel('$g_2$')
        ax3.set_xlabel('$q (nm^{-1})$'); ax3.set_ylabel('$\\beta$')
        ax4.set_xlabel('$q (nm^{-1})$'); ax4.set_ylabel('$\\Gamma(q)$')
        
    ax1 = fig.add_subplot(gs[0,-1])
    ax2 = fig.add_subplot(gs[1,-1])
    
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax1, label="I(q)")
    fig.colorbar(mpl.cm.ScalarMappable(norm=normi, cmap=cmapi), cax=ax2, label="q", format=mpl.ticker.FuncFormatter(lambda x,p: "%.3e"%(qs[np.where(x == q_ranges[:,0])])), ticks=q_ranges[::((q_ranges.shape[0]//16)+1),0])
    

def plot_ttcf(file, key, idx):
    ttcf, ts, age = file.get_ttcf(key, idx)
    fig = plt.gcf()
    ax = plt.subplot(111)
    
    cmap = mpl.cm.jet
    norm = mpl.colors.Normalize(vmin=0.5, vmax=2)
    
    X,Y = np.meshgrid(ts[1:], age)
    ax.pcolormesh(X,Y,ttcf[:,1:], cmap=cmap, norm=norm)
    
    ax.set_xscale('log')
    ax.set_xlabel('ts (s)')
    ax.set_ylabel('Age (s)')
    ax.set_title('%s / %i q=%.3e'%(key, idx, file.qs[file.get_q_index(key)[idx]-1]))
    
    fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap), label="ttcf(age,lag)")
    

def main():
    logger.setLevel(logging.DEBUG)
    file = XPCSResultFile(sys.argv[1])
    
    plt.figure(0)
    plot_SAXS_with_qranges(file)
    
    plt.figure(1)
    plot_analysis_qranges(file)
    
    for i,k in enumerate(file.analysis_keys):
        plt.figure(2)
        plot_ttcf(file, k, 3)
        break
    
    plt.show()
    
    
def _matrixAvg(x, nx_intvs, M, axis):
    """
    Resample a matrix along specific axis
    
    :param x: Axis coordinates. Have to be strictly increasing.
    :param nx_intvs: Intervals at which the matrix will be sliced
    :param M: Matrix to be sliced
    :param axis: Axis number
    
    :return (nx, nM): New axis and new matrix
    """
    
    x = x.ravel()
    nx_intvs = nx_intvs.ravel()
    if x.shape[0] != M.shape[axis]:
        raise ValueError("Inconsistant axis coordinates with matrix.")
        
    if not np.all(np.diff(x) > 0):
        raise ValueError("x Have to be strictly increasing.")
        
    # Compute slicing indexes
    # idx = np.arange(x.shape[0])
    # sidx = []
    # for v in nx_intvs:
    #     if v < x[-1]:
    #         sidx += [idx[x > v][0],]
    #     else:
    #         sidx += [x.shape[0]-1,]
            
    # binc = np.diff(np.r_[sidx,x.shape[0]])
    # nx = np.add.reduceat(x, sidx)/binc
    # nM = np.add.reduceat(M, sidx, axis)/binc
    
    logger.debug(M)
    
    N = nx_intvs.shape[0]-1
    nx = np.zeros((N), dtype=np.float32)*np.nan
    MS = [*M.shape]
    MS[axis] = N
    nM = np.zeros(MS, dtype=np.float32)*np.nan
    # logger.debug(M.shape)
    
    idx1 = [slice(None),]*len(MS)
    idx2 = [slice(None),]*len(MS)
    MM = []
    
    for j in range(N):
        msk = np.logical_and(x >= nx_intvs[j], x < nx_intvs[j+1])
        # logger.debug(np.any(msk))
        if np.any(msk):
            nx[j] = np.nanmean(x[msk])
            idx1[axis] = j
            idx2[axis] = msk
            
            avg = np.nanmean(M.__getitem__(idx2), axis=axis)
            
            # logger.debug(avg.shape)
            
            nM.__setitem__(idx1, avg)
            
    # logger.debug((nx, nM))
    
    idxs = np.where(np.isnan(nx))
    nM = np.delete(nM, idxs, axis)
    nx = np.delete(nx, idxs, 0)
    
    return nx, nM
    
def ttcf_resample(ttcf, lag, age, lag_intervals=None, age_intervals=None):
    """
    Resample the two time correlation function, by averaging
    
    :param ttcf:            (LxA) The two time correlation function to be resampled
    :param lag:             (1XL) TTCF lag time axis
    :param age:             (1XA) TTCF age axis
    :param lag_intervals:   (1xnL+1) Bounds of new lag time axis. If none, do not rescale this axis
    :param age_intervals:   (1xnA+1) Bounds of new age axis. If none, do not rescale this axis
    
    :return (nlag, nage, nttcf): 
    """
    
    reshape = False
    if len(ttcf.shape) == 2:
        ttcf.shape = (1,*ttcf.shape)
        reshape = True
        
    lag = lag.ravel()
    age = age.ravel()
    
    if lag_intervals is not None:
        lag, ttcf = _matrixAvg(lag, lag_intervals, ttcf, 2)
        
    logger.debug("lag time done")
        
    if age_intervals is not None:
        age, ttcf = _matrixAvg(age, age_intervals, ttcf, 1)
        
    logger.debug("age done")
        
    if reshape:
        ttcf.shape = ttcf.shape[1:]
    
    return lag, age, ttcf


def ttcf_resample_npoints(ttcf, lag, age, nlag=0, nage=0, lagmode=None, agemode=None):
    """
    Resample the TTCF by specifying the number of points
    
    :param ttcf: The ttcf to be resampled
    :param lag: Lag time axis
    :param age: Age axis
    :param nlag: Number of points along the lag time axis
    :param nage: Number of points along the age axis
    :param lagmode: Mode for lag time. None for no reduction, 'lin' or 'log'.
    :param agemode: Mode for age. None for no reduction, 'lin' or 'log'.
    """
    
    lag_intervals = None
    age_intervals = None
    
    if lagmode is not None:
        if lagmode == 'lin':
            lag_intervals = np.linspace(0, np.max(lag), nlag+1)
        elif lagmode == 'log':
            msk = lag > 0
            lag_intervals = 10**np.linspace(np.log10(np.min(lag[msk])), np.log10(np.max(lag)), nlag+1)
        else:
            raise ValueError(f"Lagmode should be None, lin or log, not {lagmode}")
    
    if agemode is not None:
        if agemode == 'lin':
            age_intervals = np.linspace(0, np.max(age), nage+1)
        elif agemode == 'log':
            msk = age > 0
            age_intervals = 10**np.linspace(np.log10(np.min(age[msk])), np.log10(np.max(age)), nage+1)
        else:
            raise ValueError(f"Agemode should be None, lin or log, not {agemode}")
            
    return ttcf_resample(ttcf, lag, age, lag_intervals, age_intervals)
        
        
        
        
        
        
        
        
        
        
        
