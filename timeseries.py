import numpy as np
import subprocess as sp
import matplotlib.pyplot as plt
import npy2perseus as n2p
from pyTopTools import perseus_wrap as pers
from pyTopTools import bottleneck_distance as BD
import tempfile

"""
Module for handling time series and ndarrays for persistence analysis.

Author: Jesse Berwald

Opened: March 10, 2013
"""

class Timeseries( object ):
    """
    Basic container for data. Methods for reading, writing, analyzing.

    data : numpy array or path to file (.txt or .npy)

    data_type : cubical ('cub'), sparse cubical ('scub'), or
    vietoris-rips point cloud ('vr'). 
    """
    def __init__( self, data, data_type ):

        if hasattr( data, '__array__' ):
            self.data = data
        else:
            self.fname = data
            try:
                self.data = np.load( self.fname )
            except IOError:
                self.data = np.fromfile( self.fname, sep='\n' )

        self.dtype = data_type


    def __repr__( self ):
        s = "Timeseries with " + str( len(self.data) ) +\
            " points. min = "+str(self.data.min())+", max = "+\
            str( self.data.max() )
        return s

    def mean( self ):
        return self.data.mean()

    def var( self ):
        return self.data.var()

    def std( self ):
        return self.data.std()

    def convert2perseus( self, persname, **kwargs ):
        """
        Convert an array, or text or numpy file to perseus format.

        data -- numpy array

        Writes a 1D point cloud to Persues-readable Vietoris-Rips format.
        """
        space = " "
        fargs = {'radius_scaling' : 1,
                 'stepsize' : 0.02,
                 'nsteps' : 10,
                 'bradius' : 0.0,
                 'embed_dim' : 1
                 }
        fargs.update( kwargs )

        # fix up end of filename
        fargs['persname'] = persname
        if not fargs['persname'].endswith( 'txt' ):
            fargs['persname'] += '.txt'

        # This gets appended to the end of every line
        br = str( fargs['bradius'] )

        with open( fargs['persname'], 'w' ) as fh:
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
            for obs in self.data:
                try:
                    r = [ str( x ) for x in obs ]
                except TypeError:
                    # quicker than if/else 
                    r = [ str( obs ) ]
                r += [ br ] # add the birth radius
                r = space.join( r )
                r += '\n'
                fh.write( r )

        print "wrote file to ", fargs['persname']
        
        self.persin = fargs['persname']
        self.inf_value = fargs['nsteps']
        out = { 'filename' : fargs['persname'],
                'data' : self.data }
        return out

    def draw_data( self, **kwargs ):
        """
        Either plot the data as a time series, a scatter plot (no
        implemented) or use imshow for a matrix.
        """
        if self.data.ndim == 1:
            fig = plt.figure()
            ax = fig.gca()
            ax.plot( self.data, **kwargs )
            return fig
        elif self.dtype == 'scub' or self.dtype == 'cub':
            fig = plt.figure()
            ax = fig.gca()
            ax.imshow( self.data )
            return fig

class Window( Timeseries ):

    def __init__( self, data, tmin=0, tmax=-1, data_type='vr', dim=0 ):
        """
        data : windowed data from a time series. 

        tmin
        """
        Timeseries.__init__( self, data, data_type )
        self.tmin = tmin
        self.tmax = tmax
        if tmax == -1:
            tmax = len( data )
        if data.ndim > 1:
            self.data = data
        else:
            self.data = self.data[ tmin:tmax ]
        self.persdia = None
        self.perspath = None
        self.dim = dim
        self.diagram_dim = dim

    def compute_persistence( self, fname, output=None, dtype='brips', debug=False ):
        """
        Compute persistence topology of data cloud using Perseus on
        the VR complex in fname.
        """
        # prefix for the persistence diagram files
        if not output:
            if fname.endswith( '.txt' ):
                output = fname[:-4]
        pers.perseus( fname, output, dtype, debug=debug )

        # load diagram for the level we're interested in
        try:
            self.persdia = np.loadtxt( output + '_' + str( self.diagram_dim ) + '.txt' )
        # disk latency, if lots of IO, can cause a delay in the buffer
        # flushing to disk, and hence a "file does not exist error"
        except IOError:
            time.sleep( 1 )
            self.persdia = np.loadtxt( output + '_' + str( self.diagram_dim ) + '.txt' )
            
        self.perspath = output # prefix, must append dim and .txt

    def compute_bottleneck_distance( self, other, this_dia=None,
                                     return_match=False, engine='c' ):
        """
        Compute the bottleneck distance between this the persistence
        diagram for this data and a diagram for 'other'.

        Diagram for this Window object must have been computed already.

        this_dia : path to this window's persistence diagram data
        (should be stored in self.persout attribute)

        other : path to persdia file
        """
        if this_dia is None:
            this_dia = self.perspath

        this_dia += '_' + str(self.diagram_dim) + '.txt'
        other += '_' + str(self.diagram_dim) + '.txt'
        try:
            dist = sp.check_output( ["bottleneck", this_dia, other] )
        except:
            print "subprocess returned an error!"
        return dist

    def compute_wasserstein_distance( self, other, this_dia=None ):
        """Compute the Wasserstein distance between self.persdia and other.

        Diagram for this Window object must have been computed
        already.

        this_dia : path to this window's persistence diagram data
        (should be stored in self.persout attribute)

        other : path to persdia file
        """
        if this_dia is None:
            this_dia = self.perspath
            
        this_dia += '_' + str(self.diagram_dim) + '.txt'
        other += '_' + str(self.diagram_dim) + '.txt'
        try:
            dist = sp.check_output( ["wasserstein", this_dia, other] )
        except:
            print "subprocess returned an error!"
        return dist
        
    def draw_diagram( self, fname=None, fig=None, scale=1, dim=None, **args ):
        """fname : full path to persistence diagram file. 
        
        fig : Figure object, in case we want to plot diagram on top of
        one another (for some reason...)

        scale : This scales (birth,death) pairs. Written for Morse
        function version of persistence. But useful in that the
        plot_diagram_scaled() function also plots markers whose size
        is determined by the number of generators at that (b,d)
        coordinate.

        """
        if dim is None:
            dim = self.diagram_dim

        # self.perspath was set in compute_wasserstein_distance()
        if fname is None:
            fname = self.perspath + '_' + str( dim ) + '.txt'

        if scale:
            fig = pers.plot_diagram_scaled( fname, scale=scale, fig=fig,
                                            inf_value=self.inf_value, **args )
        # if not scale:
        #     fig = pers.plot_diagram( fname, fig=fig, **args )
        # else:
           
        return fig

class WindowND( Window ):
    """
    Implements specialized methods for writing ndarrays to Perseus
    format. 
    """
    def __init__( self, data, data_type='vr', diagram_dim=1 ):
        Window.__init__( self, data, data_type )
        self.dim = data.ndim
        self.diagram_dim = diagram_dim

    def __repr__( self ):
        s = "WindowND timeseries with " +str( len(self.data) )+ \
            " points in R^"+str( self.dim )
        return s
        
    # this trumps the method in Timeseries class
    def convert2perseus( self, persname, **kwargs ):
        """
        Convert an array, or text or numpy file to perseus format.

        data -- numpy array

        Writes a 1D point cloud to Persues-readable Vietoris-Rips format.
        """
        space = " "
        fargs = {'radius_scaling' : 1,
                 'stepsize' : 0.02,
                 'nsteps' : 10,
                 'bradius' : 0.0,
                 'embed_dim' : self.dim
                 }
        fargs.update( kwargs )

        # fix up end of filename
        fargs['persname'] = persname
        if not fargs['persname'].endswith( 'txt' ):
            fargs['persname'] += '.txt'

        # This gets appended to the end of every line
        br = str( fargs['bradius'] )

        with open( fargs['persname'], 'w' ) as fh:
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
            for obs in self.data:
                try:
                    r = [ str( x ) for x in obs ]
                except TypeError:
                    # quicker than if/else 
                    r = [ str( obs ) ]
                r += [ br ] # add the birth radius
                r = space.join( r )
                r += '\n'
                fh.write( r )

        print "wrote file to ", fargs['persname']

        # store some constant values
        self.persin = fargs['persname']
        self.inf_value = fargs['nsteps']
        out = { 'filename' : fargs['persname'],
                'data' : self.data }
        return out


    def draw_data( self, **kwargs ):
        """
        Only implemented for 2D (maybe later for 3D).
        """
        fargs = { 'ms': 2,
                  'color' : 'b',
                  'marker' : '.'
                  }
        fargs.update( kwargs )

        if self.dim == 2:
            fig = plt.figure()
            ax = fig.gca()
            cs = fargs['color'] + fargs['marker']
            ax.plot( self.data[:,0], self.data[:,1], cs, 
                     **fargs )
            return fig
        else:
            print "Data must be 2D!"


    
# Handy functions, but general enough to be left out of the above classes
def moving_average( X, window_size, mode='same' ):
    """
    Computes the moving average over the time series X, with a moving
    window of size 'window_size'.

    See np.convolve() for help with 'mode'.
    """
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve( X, window, mode=mode)
