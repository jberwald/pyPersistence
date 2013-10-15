"""
Module to convert numpy array to various Persues formats.
"""

import numpy as np
import matplotlib.pylab as plt
import re
import os
import pickle as pkl
#from scipy.spatial import distance
from itertools import izip

space = ' '  # for strings

def write_cubtop( arr, output, scale=1, dtype=None ):
    """
    Write an array of values to dense cubical toplex Perseus format.

    Note: Only implemented for dims 1 and 2.
    """
    min_val = arr.min()
    if min_val < 1:
        arr += abs( min_val ) + 1

    # For *cub formats it 's necessary to rescale and take the ceil
    # (or floor)
    if scale != 1:
        arr *= scale
    if dtype is not None:
        arr = np.asarray( arr, dtype=dtype )    
        
    with open( output, 'w' ) as fh:
        fh.write( str( arr.ndim )+'\n' )
        # row and column dims for Perseus memory alloc
        for d in range( arr.ndim ):
            fh.write( str( arr.shape[d] ) + '\n' )

        if arr.ndim == 1:
            for x in arr:
                fh.write( str( x ) + '\n' )
        else:
            # write every value to disk
            for i in xrange( arr.shape[0] ): 
                for j in xrange( arr.shape[1] ):
                    # round to nearest integer
                    fh.write( str( int( arr[i,j] ) ) + '\n' )
    return output

def write_scubtop( arr, output, ndim=2 ):
    """
    Write an array to *sparse* Perseus format.
    
    arr -- numpy ndarray

    output -- name (full path) of output file

    NOTE -- Only implemented for arr.ndim == 2.
    """
    with open( output, 'w' ) as fh:
        fh.write( str( arr.ndim )+'\n' )
        for i in xrange( arr.shape[0] ): 
            for j in xrange( arr.shape[1] ):
                if int( arr[i,j] ) != 0:
                    pos = str(i) + ' ' + str(j) + ' '
                    fh.write (pos + str(int( arr[i,j] )) + "\n")
    return output

def write_scubtop_ND( arr, output ):
    """
    arr : numpy ndarray

    output : name (full path) of output perseus-readable file
    """
    space = ' '
    with open( output, 'w' ) as fh:
        fh.write( str( arr.ndim ) + '\n' )
        w = np.where( arr != 0 )
        # iterator over all non-zero coordinates in arr
        all_nz = izip( *w )
        for nz in all_nz:
            pos = map( str, nz )
            pos.append( str( int(arr[nz]) ) )
            pos.append( '\n' )
            fh.write( space.join( pos ) )      
    

def write_vr( data, **kwargs ):
    """
    data -- numpy array

    Writes a point cloud to a Persues-readable Vietoris-Rips format.
    """
    fargs = {'output' : None,
             'radius_scaling' : 1,
             'stepsize' : 0.2,
             'nsteps' : 10,
             'bradius' : 0.1,
             'tstepsize' : 1,
             'embed_dim' : 1
             }
    fargs.update( kwargs )

    if not fargs['output'].endswith( 'txt' ):
        fargs['output'] += '.txt'

    # This gets appended to the end of every line
    br = str( fargs['bradius'] )

    with open( fargs['output'], 'w' ) as fh:
        # ambient dimension
        fh.write( str( fargs['embed_dim'] )+'\n' )

        # initial threshold, step size, num steps, dimension cap==ny
        params = [ str( fargs['radius_scaling'] ),
                   str( fargs['stepsize'] ),
                   str( fargs['nsteps'] )
                   ]
        params = space.join( params )
        params += '\n'
        fh.write( params )

        # now write the timeseries and birth radii to disk
        for obs in data:
            try:
                r = [ str( x ) for x in obs ]
            except TypeError:
                # quicker than if/else 
                r = [ str( obs ) ]
            r += [ br ] # add the birth radius
            r = space.join( r )
            r += '\n'
            fh.write( r )
    print "wrote file to ", fargs['output']
    out = { 'filename' : fargs['output'],
            'data' : data }
    return out


def write_distance_mat( dmat, outname=None, **kwargs ):
    """
    data : distance or correlation matrix (must be square). 

    Out written for use with command:
    
    $ perseus distmat <path to distance matrix file> <output string>

    File has the following structure, omitting everything after ':', 

    (line 1)
    3: this is the number of rows/columns in the symmetric distance matrix 
    
    (line 2)
    0.1 0.2 5 2: initial threshold distance g = 0.1, step size s =
    0.2, number of steps N = 5 and dimension cap C = 2
 
    (line 3) 
    0 0.26 0.4: distance from entry 1 to itself, entry 2, entry 3 
    0.26 0 2.1: distance from entry 2 to entry 1, itself and entry 3, 
    0.4 2.1 0: etc.
    """
    fargs = { 'dimcap' : 2,
              'g_thresh' : 0.1,
              'stepsize' : 0.2,
              'nsteps' : 5
              }
    fargs.update( kwargs )
    space = " "
    
    # num points x dimension
    nx, ny = dmat.shape

    # create temp file if necessary
    if outname is None:
        fh = tempfile.NamedTemporaryFile(delete=False)
    else:
        if not outname.endswith( 'txt' ):
            outname += '.txt'
        fh = open( outname, 'w' )

    # nx x nx distance matrix
    fh.write( str( nx )+'\n' )

    # initial threshold, step size, num steps, dimension cap==ny
    params = [ str( fargs['g_thresh'] ), 
               str( fargs['stepsize'] ), 
               str( fargs['nsteps'] ), 
               str( fargs['dimcap'] ) ]
    params = space.join( params )
    params += '\n'

    # write the top lines with parameters
    fh.write( params )
    
    # now write each row (not optimized)
    for row in dmat:
        r = [ str( x ) for x in row ]
        r = space.join( r )
        r += '\n'
        fh.write( r )

    fh.close() 
    print "Wrote distance/correlation matrix to", outname

