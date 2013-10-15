import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
import npy2perseus as n2p
import perseus as pers
import scipy.io as sio
"""
Module for handling miscellaneous opeations with persistence diagrams,
mainly plotting.

Author: Jesse Berwald

Opened: Oct 15, 2011
"""
def plot_diagram( diagram, fontsize=12, scale=None, color='b',
                  inf_value=None, show_fig=True, fig=None, title=None ):
    """
    diagram -- path to <perseus output>_*.txt, where * is the dimension.

    scale -- Factor to scale the birth/death times. 
    """
    if hasattr( diagram, '__array__' ):
        s = diagram
    else:
        if scale:
            # cast values as floats for division
            s = np.loadtxt( diagram, dtype=np.float, delimiter=' ' )
            s /= scale
        else:
            s = np.loadtxt( diagram, dtype=np.int, delimiter=' ' )
        
    try:
        births = s[:,0]
        deaths = s[:,1]
    except IndexError:
        # s is an (n,) array, so it must be reshaped in-place for
        # proper indexing
        print s.shape
        s.resize( ( s.shape[0], 1 ) )
        print s
        births = s[0] 
        deaths = s[1]

    # max death time
    if deaths.max() > 0:
        if inf_value==None:
            maxd = deaths.max()
        else: 
            maxd = inf_value
    else:
        maxd = births.max()
    print "Max death time ",  maxd
  
    # non-infinite gens
    normal_idx = np.where( deaths != -1 )[0]

    # add to an existing figure if necessary
    if not fig:
        fig = plt.figure( ) 
        fig.patch.set_alpha( 0.0 )
    ax = fig.gca()

    if len( normal_idx ) > 0:
        ax.plot( births[normal_idx], deaths[normal_idx], color+'o' )

    # create diagonal
    diag = [0, maxd+1]
    ax.plot(diag, diag, 'g-')

    # infinite gens
    inf_idx = np.where( deaths == -1 )[0]
    inf_vec = (maxd + 1) * np.ones( len( inf_idx ) )

    # plot the infinite generators
    ax.plot( births[inf_idx], inf_vec, 'ro' )
    # xticks = [ int( tk ) for tk in ax.get_xticks() ]
    # yticks = [ int( tk ) for tk in ax.get_yticks() ]
    ax.set_xticklabels( ax.get_xticks(), fontsize=fontsize )
    ax.set_yticklabels( ax.get_yticks(), fontsize=fontsize )
    ax.set_xlabel( 'birth', fontsize=fontsize )
    ax.set_ylabel( 'death', fontsize=fontsize )
    # fix the left x-axis boundary at 0
    ax.set_xlim( left=0 )
    ax.set_ylim( bottom=0 )

    if title:
        ax.set_title( title, fontsize=16 )
    if show_fig:
        fig.show()
        
    print "Total number of persistence intervals", len( births ) 
    return fig


def find_unique( arr ):
    """
    arr : 1D array 

    Returns indices of (first occurence of) unique elements in arr
    """
    uniq = np.unique( arr )
    idx = [ np.where( arr==x )[0] for x in uniq ]
    return idx


def plot_diagram_scaled( diagram, fontsize=12, scale=None, color='b',
                         show_fig=True, fig=None, title=None, resize=False,
                         inf_value=None, marker_scale=1, show_legend=False, **args ):
    """
    This is the smae as plot_diagram(), except that each point on the
    diagram is scaled in relation to its number of occurences in the
    persistence diagram multiset. Thus, a birth-death pair will garner
    a larger marker if there are a realtively large number of unique
    generators with the same birth-death coordinates.
    
    persFile -- path to <perseus output>_*.txt, where * is the dimension.

    scale -- Factor to scale the birth/death times.

    marker_scale -- Factor by which to scale marker sizes.
    """
    if hasattr( diagram, '__array__' ):
        s = diagram
    else:
        if scale:
            # cast values as floats for division
            s = np.loadtxt( diagram, dtype=np.float, delimiter=' ' )
            s /= scale
        else:
            s = np.loadtxt( diagram, dtype=np.int, delimiter=' ' )
        
    try:
        births = s[:,0]
        deaths = s[:,1]
    except IndexError:
        # s is an (n,) array, so it must be reshaped in-place for
        # proper indexing
        print s.shape
        s.resize( ( s.shape[0], 1 ) )
        print s
        births = s[0] 
        deaths = s[1]

    # max death time
    if deaths.max() > 0:
        if inf_value==None:
            maxd = deaths.max()
        else: 
            maxd = inf_value
    else:
        maxd = births.max()
    print "Max death time ",  maxd

    # non-infinite gens
    normal_idx = np.where( deaths != -1 )[0]

    # find indices of unique birth-death coords.
    # [1] index just pulls off the indices
    uniq_idx = find_unique( deaths[normal_idx] )

    # add to an existing figure if necessary
    if not fig:
        fig = plt.figure( ) 
        fig.patch.set_alpha( 0.0 )
    try:
        ax = fig.gca()
    # in case we pass in the axes instance itself
    except AttributeError:
        ax = fig

    if len( normal_idx ) > 0:
        for u in uniq_idx:
            if resize:
                size = marker_scale*len( u )
            else:
                size = marker_scale
            ax.plot( births[ u ], deaths[ u ],
                     color+'o', ms=size, alpha=0.8 )
            # ax.plot( births[normal_idx], deaths[normal_idx], ,
            #          color+'o', )

    # create and plot the diagonal
    diag = [0, maxd+2]
    ax.plot(diag, diag, 'g-')

    # infinite gens
    inf_idx = np.where( deaths < 0 )[0]
    inf_vec = (maxd + 1) * np.ones( len( inf_idx ) )

    # plot the infinite generators
    ax.plot( births[inf_idx], inf_vec, 'ro', 
             label='Robust generators (num=' + str(len(inf_idx) ) + ')', 
             **args )
    # xticks = [ int( tk ) for tk in ax.get_xticks() ]
    # yticks = [ int( tk ) for tk in ax.get_yticks() ]
    ax.set_xticklabels( ax.get_xticks(), fontsize=fontsize )
    ax.set_yticklabels( ax.get_yticks(), fontsize=fontsize )
    ax.set_xlabel( 'birth', fontsize=fontsize )
    ax.set_ylabel( 'death', fontsize=fontsize )
    # fix the left x-axis boundary at 0
    ax.set_xlim( left=0, right=maxd+2 )
    ax.set_ylim( bottom=0, top=maxd+2 )

    # legend displaying number of robust/infinite generators
    if show_legend:
        ax.legend( loc=4 ) # 4 == lower right
    
    if title:
        ax.set_title( title, fontsize=16 )
    if show_fig:
        fig.show()
        
    print "Total number of persistence intervals", len( births ) 
    return fig


## Useful conversion routines
def diagrams2cellarray( dia_list, outname, chop_inf=True, mat_type=np.float ):
    """dia_list : n-length list of k x 2 diagrams

    outname : name of output file. '.mat' will be automatically appended.

    Optional:
    --------

    chop_inf : Remove the row corresponding to the infinite generator.

    mat_type : some matlab programs expect a certain data type for
    diagrams (eg. Error using '+' will be thrown). defaults to
    double. Standard options should diverge far from np.int, np.float,
    np.int64, etc.

    Recipe from http://docs.scipy.org/doc/scipy/reference/tutorial/io.html#matlab-cell-arrays

    """
    n = len( dia_list )
    # object array to hold different length diagrams. Exclude the last
    # (inf) generator if chop_inf==True.
    C = np.zeros( (n,), dtype=np.object )
    
    for i,d in enumerate( dia_list ):
        # exclude last row
        if chop_inf:
            d = d[:-1]
        if d.dtype != mat_type:
            d = d.astype( mat_type )
        C[i] = d
    sio.savemat( outname+'.mat', { 'diagrams': C } )
    
def cellarray2diagrams( matfile, matname='means' ):
    """
    Read in a matlab file containing a cell array. 
    
    matfile : path to .mat file

    Optional:
    --------

    matname : name of stored variable. Default = 'means'

    Returns dictionary of { 'cell' : mean diagram }
    """
    
    cellarray = sio.loadmat( matfile )
    
    # N x 2 object array, with dict key in first column and dict value
    # an Mx2 array in second column. 
    mat = cellarray[ matname ]
    mdict = dict()
    
    # line up key/value pairs as a dict
    for name, arr in mat:
        # convert from unicode -> ascii
        name = name.item()
        cell = name.encode( 'ascii' )
        mdict[ cell ] = arr

    return mdict

