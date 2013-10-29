'''
Created on Jan 19, 2013

This code computes the Wasserstein distance between two diagrams,
as well as running the gradient descent algorithm from:

Frechet Means for Distributions of Persistence diagrams
Katharine Turner, Yuriy Mileyko, Sayan Mukherjee, John Harer
http://arxiv.org/abs/1206.2790



'''

import numpy as np

# cython
cimport numpy as np

from cpython cimport bool

# fix array dtype and also a corresponding compile-time _t type
DTYPE = np.float
ctypedef np.float_t DTYPE_t

#import munkres as munk
import _hungarian as h

import random
import pickle
#import matplotlib.pyplot as plt


# Cython version of dist function
cdef float cydist( np.ndarray[DTYPE_t, ndim=1] a, 
                   np.ndarray[DTYPE_t, ndim=1] b, 
                   bool bottleneck ):
    """
    This is a modified Wasserstein, using 'internal' norm that is
    L2, not L_\infty.

    We use -2 to signify elements that were labeled 'Diag' in dist().

    Returns L2 or L_\infty distance between diagram points.
    """
    # minimal type checking
    assert a.dtype == DTYPE and b.dtype == DTYPE
   # insideDistance=np.linalg.norm

    cdef DTYPE_t dist
    cdef int i

    if a[0] == -2:
        if b[0] == -2:
            dist =  0.
        else:
            if bottleneck:
                dist = b[1] - b[0]
            else:
                dist = (b[1]-b[0]) / np.sqrt(2)
    else:
        if b[0] == -2:
            if bottleneck:
                dist = a[1] - a[0] 
            else:
                dist = np.sqrt( (a[1]-a[0])**2/2. )
        else:
            if bottleneck:
                dist = max( [ b[i] - a[i] for i in range(2) ] )
            else:
                dist = np.linalg.norm([b[i]-a[i] for i in range(2)])
    return dist


def WassDistDiagram( D, E, p=2, bottleneck=False, returnPairing = False):
    '''
    Determines pairwise distances between all pairs of points in diagrams D and E
    Diagrams should be entered as lists of off-diagonal points, but could have 'Diag.
    
    EDIT: Diagrams could potential have None value as an off-diagonal point.
    We need to keep track of these so that the pairings line up for mean distribution 
    necessity, but this should return the same answer up to renumber if there are no
    None values.
    
    
    If returnPairing == True, this wil also return the actual pairing used for the 
    Wass distance
    '''
    # Cython static types
    cdef int i
    cdef int j   
    cdef float cyd
    cdef float cye 
    cdef float wass_p = p
    cdef int k = len(D)
    cdef int l = len(E)
    cdef DTYPE_t answer
    
    # lists for initial construction of edges
    D = D[:]    #Necessary to not edit the diagram at the higher level
    E = E[:]
    
    # extend D,E by diagonal vertices -2 => 'DIAG'
    D.extend([[-2.,-2.] for i in range(l)])
    E.extend([[-2.,-2.] for i in range(k)])
        
    # convert D, E to arrays for cython speed
    cdef np.ndarray[DTYPE_t, ndim=2] cyD = np.zeros( (k+l,2), dtype=DTYPE )
    cdef np.ndarray[DTYPE_t, ndim=2] cyE = np.zeros( (k+l,2), dtype=DTYPE )

    # fill cyD, cyE with  pairings
    for i in range( k+l ):
        for j in range( 2 ):
            cyD[i,j] = D[i][j]
            cyE[i,j] = E[i][j]

    # container for pair weights
    cdef np.ndarray[DTYPE_t, ndim=2] M = np.zeros( [k+l,k+l], dtype=DTYPE )
    
    # distance computations for the extended diagrams in D,E
    for i in range( k+l ):
        for j in range( k+l ):
            if bottleneck:
                M[i,j] = cydist( cyD[i], cyE[j], bottleneck )
            else:
                M[i,j] = cydist( cyD[i], cyE[j], bottleneck )**wass_p

    # optimization step using Hungarian/Hopcroft-Karp
    N = M.tolist()
    pairs = zip(range(len(D)), h.hungarian(N))

    answer = 0.
    if not bottleneck: 
        for pair in pairs:
            answer += M[pair[0],pair[1]]
        answer = (answer)**(1./p)
    # bottleneck
    else:
        pair_values = [ M[pair[0],pair[1]] for pair in pairs ]
        answer = max( pair_values )

    if returnPairing:
        '''
        Returns pairs used for distance.
        If one of the entries in the diagram is 'Diag', it does not return 
        a specific pair for that one: All pairs are of the form:
        A) [i,j]
        B) [i, 'Diag']
        C) ['Diag', j]
        '''
        PairsEdit = []
        for p in pairs:
            p = list(p)
            
            # cython: -2 <==> 'Diag'
            if cyD[p[0],0] == -2:
                p[0] = 'Diag'
            
            if cyE[p[1],0] == -2:
                p[1] = 'Diag'
            
            if not p[0] == 'Diag' or not p[1] == 'Diag':
                PairsEdit.append(p)
            
            #===================================================================
            # if p[0]< k:
            #    if p[1]<l:
            #        PairsEdit.append(p)
            #    else:
            #        PairsEdit.append([p[0],'Diag'])
            # else:   #p[0] must be diagonal
            #    if p[1] < l:
            #        PairsEdit.append(['Diag',p[1]])
            #    else:
            #        pass    #both are beyond marked points, so don't add
            #===================================================================

        
        return answer, PairsEdit
    else:
        return answer
    

#===============================================================================
# 
# 
# def drawDiagram(d, color = 'purple',size = 10):
#    x = [round(p[0],2) for p in d if not p == 'Diag']
#    y = [round(p[1],2) for p in d if not p == 'Diag']
# 
#    plt.scatter(x, y, color = color, s = size)
# 
# 
# 
#===============================================================================




