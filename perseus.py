import subprocess as sp
import numpy as np
from numpy import loadtxt, load
import matplotlib.pyplot as plt
import argparse
import os

space = " "
slash = "/"

def perseus ( fname, output, dtype='scubtop', path=None, debug=False ):
    """
    Call perseus with the command

    '$ perseus DTYPE FNAME OUTPUT'

    (Note, perseus must be in you PATH)

    fname -- full path data file

    output -- prefix of output file, will be appended with
        output_*.txt by perseus

    dtype -- input to perseus, eg., cubtop, scubtop, etc.

    See http://www.math.rutgers.edu/~vidit/perseus.html for more
    details.
    """
    if os.uname()[0] == 'Darwin':
        cmd = [ '/usr/bin/perseus3', dtype, fname, output ]
    else:
        cmd = [ 'perseus', dtype, fname, output ]

    if debug:
        print "Command: "
        print cmd
    try:
        result = sp.call( cmd )
    except OSError:
        print "subprocess failed!"
        print "command passed to subprocess:", cmd
    return result

def convert2perseus( data, dtype, **kwargs ):
    """
    Convert an array, or text or numpy file to perseus format.
    """
    if dtype == 'dmatrix':
        out = write_distance_matrix( data, **kwargs )
    elif dtype == 'timeseries':
        out = write_timeseries( data, **kwargs )
    else:
        print "Unknown data type!"
    return out

def write_time_series( data, **kwargs ):
    """
    data -- numpy array

    Writes a time series to a Persues-readable Vietoris-Rips format.
    """
    fargs = {'output' : None,
             'radius_scaling' : 1,
             'stepsize' : 0.2,
             'nsteps' : 10,
             'bradius' : None,
             'tstepsize' : 1,
             'embed_dim' : 1
             }
    fargs.update( kwargs )

    # load from file if data is not an array of points already
    if not hasattr( data, '__index__' ):
        # .npy or .txt
        try:
            data = load( data )
        except IOError:
            data = loadtxt( data )

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

        # now write the time series and birth radii to disk
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
