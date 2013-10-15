import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm

import filter_data as FD
from diagram import PersistenceDiagram

def test_PerseusProcessor( dtype='scubtop' ):
    """
    """
    from examples import gaussian as G

    persfile = './examples/PERSTEST.txt'
    persout = './examples/PERSOUT'
    matfile = './examples/gauss_trough.txt'  

    data = np.loadtxt( matfile )

    # initialize PP object
    P = FD.PerseusProcessor( data )
    
    print "Testing write_perseus() for dtype=", dtype
    print "-----"
    P.write_perseus( persfile, dtype=dtype )
    
    print "Calling Perseus on", persfile
    P.run_perseus( persout )
    print "Success!"    
    print "-----"

    return P


def test_correlation( corrmat, dimcap=2, dtype='corrmat' ):
    """
    """
    from examples import gaussian as G

    persfile = './examples/CORRTEST.txt'
    persout = './examples/CORROUT'

    # correlation matrix
    data = np.loadtxt( corrmat )

    # initialize PP object
    P = FD.PerseusProcessor( data )
    
    print "Testing write_perseus() for dtype=", dtype
    print "-----"
    P.write_perseus( persfile, dtype=dtype, dimcap=dimcap )
    
    print "Calling Perseus on", persfile
    P.run_perseus( persout, dtype=dtype )
    print "Success!"    
    print "-----"

    return P

def generate_test_data():
    """
    Borrowed from http://matplotlib.org/examples/mplot3d/contourf3d_demo2.html
    """
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y, Z = axes3d.get_test_data( 0.1 )
    Z = np.abs( Z )

    ax.plot_surface(X, Y, Z, rstride=8, cstride=8, alpha=0.3)
    cset = ax.contourf(X, Y, Z, zdir='z', offset=-10, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='x', offset=-40, cmap=cm.coolwarm)
    cset = ax.contourf(X, Y, Z, zdir='y', offset=40, cmap=cm.coolwarm)

    ax.set_xlabel('X')
    ax.set_xlim(-40, 40)
    ax.set_ylabel('Y')
    ax.set_ylim(-40, 40)
    ax.set_zlabel('Z')
    ax.set_zlim(-1, 100)

    plt.show()

    return Z

if __name__ == "__main__":

    test1 = True
    test2 = False

    if test1:
    ##############################################
        # In which we test the PerseusProcessor class
        ###############################################
        print "Testing core functionality of filter_data.PerseusProcessor..."
        print ""
        pers = test_PerseusProcessor()

        print "Figure 1a: Plotting the sum of Gaussians (from above)"
        plt.subplot( 2, 1, 1 )
        plt.imshow( pers.data )
        plt.title( 'Heat map of the sum of Gaussians', fontsize=14 )
        plt.show()
        print "-----"

        print "Figure 1b: A slice across the middle, showing the 'rim structure'"
        plt.subplot( 2, 1, 2 )
        plt.plot( pers.data[200,:], lw=2 )
        plt.title( 'Slice along row 200 of Figure 1', fontsize=14 )
        plt.show()

        print "-----"
        print ""    

        ####################################################
        # In which we test the PersistenceDiagram class
        ####################################################
        print "Testing core functionality of diagram.PersistenceDiagram..."

        # first, extract the diagram from PerseusProcessor object
        dim = 1 # this is the only interesting dimension for this data
        dia = pers.load_diagram( dim )
        print "Loaded diagram from disk"

        P = PersistenceDiagram( dia )

        print P
        print "--> There are many generators with lifespans of 1 at the top of the rim due"+\
            " numerical error in adding circular Gaussians on a square grid."
        print ""
        print "(truncated diagram array, entries 70 - 85"
        print P.diagram[70:]

        print ""
        print "-----"
        print "The numerical noise can be seen in the dot (multiset actually) "+\
            "on the diagonal of Figure 2."
        print "-----"
        print "--> The interesting features are the two off-diagonal elements associated "+\
            "with the central peak and rim (see Fig 1b)."
        P.draw_diagram()

    if test2:
        ########################################################
        # In which we test the classes for correlation matrices
        ########################################################    
        # Since the correlation matrix gives general 'distances'
        # between points, we must cap the possible dimensions of out
        # simplices.
        max_dim = 3

        print "Generating test data, we'll normalize the z-coordinate to "+\
            "get a test correlation matrix."
        C = generate_test_data()
        C /= (C.max() + 5 )

        print "-----"
        print "Figure 3 is just the correlation matrix, plotted as a heat map."
        plt.figure()
        plt.imshow( C, cmap=cm.coolwarm )
        plt.colorbar()
        plt.show()

        # save to disk
        np.savetxt( './examples/corrmat.txt', C )

        print ""
        print "-----"
        print "Filtering data using PerseusProcessor, creating diagrams"
        pers_corr = test_correlation( './examples/corrmat.txt', 
                                      dimcap=max_dim,
                                      dtype='corrmat' )

        diagrams = []
        for d in range( max_dim+1 ):
            dia = pers_corr.load_diagram( dim=d ) 
            diagrams.append( PersistenceDiagram( dia, dim=d ) )
        print "-----"
        print "Loaded diagrams from disk"
        print ""

        print "Drawing diagrams..."
        for dia in diagrams:
            dia.draw_diagram( title='Dim '+ str(dia.diagram_dim)+\
                                  ' homology', fontsize=14 )
        
