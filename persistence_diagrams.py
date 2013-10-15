"""
perisstence_diagrams.py

author: Jesse Berwald

opened: September 20, 2013

Container for operations on persistence diagrams. Eg.,

- bottleneck and wasserstein distances
- diagram plotting

"""
import numpy as np
import subprocess as sp
import tempfile
import matplotlib.pyplot as plt

# local stuff
import perseus as pers
import persistence_tools as pt



class Diagram( object ):
    """
    Base class. 

    input: Perseus diagram output at a given
    dimension. filename_'dim'.txt
    """
    def __init__( self, diagram, dim=None, inf=None ):
        """
        diagram : full path to diagram file on disk, or array
        containing diagram information.

        dim : [optional] We can extract this from the filename if
        necessary.
        """
        # diagram is an array, so save a temp file for distance
        # functions to read
        if hasattr( diagram, '__array__' ):
            fh = tempfile.NamedTemporaryFile(delete=False)
            np.savetxt( fh, diagram )
            self.dname = fh.name
            self.diagram = diagram
        else:
            self.dname = diagram
            # in case we need the data for other applications
            self.diagram = np.loadtxt( diagram )
        
        # the 'infinite' value usually comes from the maximum number
        # of steps in growing epsilon balls (say). If we don't have
        # this, then set inf to be the max death time +1
        if inf == None:
            self.inf_value = max( self.diagram[:,1] ) + 1

        self.diagram_dim = dim

    def __repr__( self ):
        s = "Persistence diagram with "+ str( len( self.diagram ) ) +\
            " generators"
        if self.diagram_dim is not None:
            s += " in dimension "+ str( self.diagram_dim )
        return s

    def compute_bottleneck_distance( self, other ):
        """
        Compute the bottleneck distance between this the persistence
        diagram for this data and a diagram for 'other'.

        Diagram for this Window object must have been computed already.

        this_dia : path to this window's persistence diagram data
        (should be stored in self.persout attribute)

        other : path to persdia file

        engine refers to either Miro's code ('c') or Kelly's
        ('python'). Not implemented.
        """
        # we need the name of the diagram file on disk for the
        # distance code
        this_dia = self.dname
        # grab the filename of the diagram if necessary
        if hasattr( other, 'dname' ):
            other = other.dname 
        try:
            dist = sp.check_output( ["bottleneck", this_dia, other] )
        except:
            print "subprocess returned an error!"
        return float( dist )

    def compute_wasserstein_distance( self, other ):
        """Compute the Wasserstein distance between self.persdia and other.

        Diagram for this Window object must have been computed
        already.

        this_dia : path to this window's persistence diagram data
        (should be stored in self.persout attribute)

        other : path to persdia file
        """
        this_dia = self.dname
        # grab the filename of the diagram if necessary
        if hasattr( other, 'dname' ):
            other = other.dname 
        try:
            dist = sp.check_output( ["wasserstein", this_dia, other] )
        except:
            print "subprocess returned an error!"
        return float( dist )
        
    def draw_diagram( self, fig=None, scale=None, dim=None, **args ):
        """fname : full path to persistence diagram file. 
        
        fig : Figure object, in case we want to plot diagram on top of
        one another (for some reason...)

        scale : This scales (birth,death) pairs. Written for Morse
        function version of persistence. But useful in that the
        plot_diagram_scaled() function also plots markers whose size
        is determined by the number of generators at that (b,d)
        coordinate.

        """
        if scale is None:
            scale = 10
        # fig = plot_diagram_scaled( self.diagram, scale=scale, fig=fig,
        #                            inf_value=self.inf_value, **args )

        fig = pt.plot_diagram( self.diagram, fig=fig,
                               inf_value=self.inf_value, **args )
           
        return fig

