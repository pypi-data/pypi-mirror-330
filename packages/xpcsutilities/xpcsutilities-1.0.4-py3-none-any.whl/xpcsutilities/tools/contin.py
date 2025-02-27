# -*- coding: utf-8 -*-



import numpy as np
import scipy.optimize as opt


def LT(s, G, tau):
    """
    Compute the discrete laplace transform (DLT) of G(s) over tau
    
    :param s: Laplace variable (s)
    :param G: Function to compute the DLT, defined on s
    :param tau: Coodinates where to evaluate the DLT (s)
    
    :return: The Discrete Laplace Transform of G
    """
    
    tau = np.array(tau).ravel()
    s = np.array(s).ravel()
    G = np.array(G).ravel()
    
    tau.shape = (tau.shape[0],1)
    s.shape = (s.shape[0],1)
    G.shape = (s.shape[0],1)
    
    return np.trapz(G*np.exp(-tau.T/s), x=s.ravel(), axis=0)
    
def g2LT(s, G, tau, beta=1):
    """
    Compute the intensity-intensity autocorrelation function from relaxation time density
    
    :param s: Laplace variable (s)
    :param G: Relaxation time density
    :param tau: Coordinates where to evaluate the g2
    :param beta: Speckles contrast
    
    :return: The Discrete Laplace Transform of G
    """
    return beta*(LT(s, G, tau) / LT(s, G, [0]))**2
    

def contin(tau, g2, s, gamma2=.2, beta0=None, G0=None):
    """
    Compute Inverse Laplace Transform (ILT) with CONTIN method
    
    :param tau: Lag time (s)
    :param g2: Intensity-Intensity autocorrelation function
    :param s: Laplace variable
    :param gamma2: 2nd derivative weight
    :param beta0: Initial value of beta
    :param G0: Initial values of G
    
    :return: (beta, ILT)
    """
    
    def fun(G, s, tau, g2, gamma2=.2):
        """
        The function to optimize
        """
        
        beta = G[0]
        G = G[1:]
        
        # Error
        err = np.sum((g2LT(s, G, tau, beta) - g2)**2) # I dont multiply by delta tau because I want geometric weighting with tau. With logarithmic tau spacing, this is division by Delta tau, so this cancel out.
        
        # Regularization function
        reg = np.trapz((np.diff(np.diff(G)))**2, x=s[1:-1])
        
        return err + gamma2*reg
    
    if beta0 is None:
        beta0 = 1
    
    if G0 is None:
        G0 = s**0/len(s)
    
    sol = opt.minimize(fun, [beta0, *G0], (s, tau, g2, gamma2), method='trust-constr', bounds=[(0,1),] + [(0, np.inf),]*len(s))
    
    return (sol.x[0], sol.x[1:])
