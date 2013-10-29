import numpy as np

# local
import npy2perseus as n2p
import perseus

class Data( object ):
    
     def __init__( self, arr, dtype='corrmat' ):
         """
         arr : np.ndarray. 

         dtype : data type (optional) 
                 'corrmat', 'distmat', 'vr', 'scubtop', 'cubtop'
                 
                 See http://www.math.rutgers.edu/~vidit/perseus/index.html
                 for details on data type.
         """
         self.data = arr
         self.dtype = dtype

     def __repr__( self ):
         s = "Data array of shape", self.data.shape
         return s

     def write_data( self, fname ):
         np.savetxt( fname, self.data )
         print "Data successfully written to: ", fname

class PerseusProcessor( Data ):
    
    def __init__( self, data ):
        Data.__init__(  self, data )
        self.dim = data.ndim

    def write_perseus( self, outname=None, dtype='scubtop', dimcap=None, **kwargs ):                                 
        """
        Output the data in Perseus format.

        outname : name of file that will become Perseus input file 

        See http://www.math.rutgers.edu/~vidit/perseus/index.html for
        details on kwargs. See fargs for the essentials below.

        Note: Output of perseus is very sensititve to stepsize and
        nsteps. Too big or small and there will not be enough
        persistence to capture the interesting behavior in the
        data. Roughly, they depend on the inherent scale of the data.

        ** If, given a Morse function (matrix of intensity values),
           computations with Perseus take a *long* time, then consider
           changing dtype='scubtop' to dtype='cubtop'. The sparse
           matrix computations performed in the background are very
           slow if the matrix is not actually sparse.
        """
        self.persfile = outname
        if dtype == 'scubtop':
            n2p.write_scubtop_ND( self.data, outname )
        elif dtype == 'cubtop':
            n2p.write_cubtop( self.data, outname, scale )
        # these only differ on the command-line call
        elif dtype == 'distmat' or dtype == 'corrmat':
            n2p.write_distance_mat( self.data, outname, dimcap=dimcap, **kwargs )
        else:
            print "Unrecognized dtype"
            raise

    def run_perseus( self, persout, dtype='scubtop' ):
        """
        Run perseus on the data. Must run write_perseus() before calling.

        persout : Filename prefix for perseus output. 
        Eg., mypersfile --> mypersfile_d.txt,

        where d is the dimension. Note, perses add the '_*.txt'.
        """
        self.persout = persout
        perseus.perseus( self.persfile, self.persout, dtype=dtype )

    def load_diagram( self, dim ):
        """
        Read diagram of dimension 'dim'. 

        dim : dimension of diagram to load

        Returns N x 2 array of birth/death coords.
        """
        dia_name = self.persout + '_' + str( dim ) + '.txt'
        self.diagram = np.loadtxt( dia_name )
        return self.diagram 
        
