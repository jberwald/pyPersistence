from numpy import random as rand
from numpy import *
import matplotlib.pyplot as plt
from pylab import figure, matshow, show, imshow
try:
    from sage.all import *
except:
    pass

rand.seed( 1234 )

def gaussian(height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*exp(
        -(((center_x-x)/width_x)**2+((center_y-y)/width_y)**2)/2)

def dist( x1, x2, y1, y2 ):
    return (x1-x2)**2 + (y1-y2)**2

def noisy_gaussian(height, center_x, center_y, width_x, width_y, noise_level, shape):
    """Returns a gaussian function with the given parameters"""
    width_x = float(width_x)
    width_y = float(width_y)
    return lambda x,y: height*exp(
        -(((center_x-x)/width_x)**2 + ((center_y-y)/width_y)**2)/2) +\
        noise_level*rand.normal( size=shape )
       
def plot_gaussian( size_x=401, size_y=401, height=100, width=20,
                   noise_level=None, bowl=False,
                   fname=None, show_fig=False ):
    """
    Gaussian centered at (100,100). Equal width in each direction.

    fname : where should we save the fig.
    """
    nx = ny = 200
    Xin, Yin = mgrid[0:size_x, 0:size_y]
    if not noise_level:
        data = gaussian(height, nx, ny, width, width)(Xin, Yin)
        if bowl:
            gb = gaussian( 0.8*height, nx, ny, 0.6*width, 0.6*width )(Xin, Yin)
            data = data - gb
    else:
        data = noisy_gaussian(height, nx, ny, width, width, noise_level, shape=Xin.shape)(Xin, Yin)
    # crop the data
    # zd = zeros_like( data )
    # for i in range( data.shape[0] ):
    #     for j in range( data.shape[1] ):
    #         if dist( 100, i, 100, j ) < 10*width**2:
    #             zd[i,j] = 1
    # data = zd * data

    # convert data into integers, just stretch stuff out 
    data = 10000 * data
    data = array( data, dtype=int )

    # if noise_level:
    #     save( "./data/gauss_bump_noise"+str(noise_level)+"_"+str(height), data )
    # else:
    #     if bowl:
    #         save( "./data/gauss_bowl_"+str(size_x), data )
    #     else:
    #         save( "./data/gauss_bump_"+str(size_y), data )
    if show_fig:
        fig = figure()
        ax = fig.gca()
        ax.matshow( data )
        return data, fig
    if fname:
        fig.savefig( fname )
        return data, fig
    else:
        return data

def sublevel( data, height, show_plt=False ):
    """
    Plot sublevel sets. Specify colors so that background is white or
    transparent.
    """
    h = height
    nx, ny = data.shape
    G = zeros( (nx,ny,3), dtype=int )
    
    G[ where( data > h ) ] = [1,1,1]
    G[ where( data <= h ) ] = [0,0,160]
    G[ where( data == 0 ) ] = [1,1,1]
    
    # now plot stuff
    fig = plt.figure( figsize=(8,8), frameon=False )
    plt.axes( frameon=False )
    ax = fig.gca()
    #ax.set_title( 'sublevel ' + str( h ) )
    ax.imshow( G, interpolation='nearest' )
    ax.set_xticks( [] )
    ax.set_yticks( [] )
    if show_plt:
        fig.show()
    return fig, G

def multi_gaussian():
    """
    Just a utility function. Requires Sage to plot results.

    Sage 3d commands:

    sage: import gaussian as gs
    sage: G = gs.multi_gaussian()
    sage: cmsel = [colormaps['jet'](i) for i in sxrange(0,1, 0.005)]
    sage: q = plot3d( lambda x,y: G[x,y], (x,0,200), (y,0,200), adaptive=True, color=cmsel)
    sage: q.show( spect_ratio=(1,1,1), figsize=[7,3], frame=False )
    """
    nx = ny = 801
    fat = plot_gaussian( nx, ny, 1.5, width=40)
    flip = plot_gaussian( nx, ny, -1.3, width=20)
    tall = plot_gaussian( nx, ny, 1, width=7)
    G = fat + flip + tall
    return G

def plot_gauss_trough( level=7430 ):
    """
    For use with sage.
    """
    G = multi_gaussian()
    #G = G / 4.
    nx,ny = G.shape

    var( 'x,y' )
    cmsel = [colormaps['jet'](i) for i in sxrange(0,1, 0.005)]
    # Q = plot3d( lambda x,y: G[x,y], (x,0,nx-1), (y,0,ny-1), adaptive=True, color=cmsel)
    # # Q.show( spect_ratio=(1,1,1), figsize=[7,3], frame=False )

    # P = plot3d( lambda x,y: level, (x,0,nx-1), (y,0,ny-1), adaptive=True, color='blue', alpha=0.5)

    # (P+Q) . show( spect_ratio=(1,1,1), figsize=[7,3], frame=True )
    Q = plot3d( lambda x,y: G[x,y], (x,100,300), (y,100,300), adaptive=True, color=cmsel)
    P = plot3d( lambda x,y: level, (x,100,300), (y,100,300), adaptive=True, color='blue', alpha=0.5)

    (P+Q) . show( spect_ratio=(1,1,1), figsize=[7,3], frame=True )

    C = clip_sublevel( G, level )
    R = plot3d( lambda x,y: C[x,y], (x,0,nx-1), (y,0,ny-1), adaptive=True, color='blue', alpha=0.5)
    
    R.show( aspect_ratio=(1,1,1), figsize=[7,3], frame=True )

    return G


def clip_sublevel( G, level ):
    """
    Set all values above 'level' to 'level.
    """
    C = G.copy()
    idx = where( G > level )
    C[ idx ] = level
    return C

def clip_below( G, lb ):
    """
    Replace all values in G < lb with 0.
    """
    w = where( G < lb )
    G[ w ] = 0
    #return G
    #return G[ w ] = 0
    
def gauss_bump( size_x=400, size_y=400, shift_x=70, shift_y=-70, noise=None ):
    """
    Create a gaussian with a small subpeak and a single pixel ("noise") raised.

    Argument 'noise' takes a float for the amplitude of the additive gaussian noise (mean 0).
    """
    nx = ny = 201
    Xin, Yin = mgrid[0:size_x, 0:size_y]

    # the big bump
    big_h = 20
    big_w = 40
    if not noise:
        big = gaussian(big_h, nx, ny, big_w, big_w)(Xin, Yin)
    else:
        big = noisy_gaussian(big_h, nx, ny, big_w, big_w,
                             noise, shape=Xin.shape )(Xin, Yin)

    # the subpeak
    small_h = 11
    small_w = 20
    snx = nx + shift_x
    sny = ny + shift_y
    small = gaussian(small_h, snx, sny, small_w, small_w)(Xin, Yin)

    # add pixelated noise at a single point near the peak of 'big'
    #if not noise:
    big[ nx-15, ny+8 ] += 1.0
    big[ nx-15, ny+9 ] += 1.0
    big[ nx-16, ny+8 ] += 1.0
    big[ nx-16, ny+9 ] += 1.0
        # big[ nx-14, ny+8 ] += 1.0
        # big[ nx-14, ny+9 ] += 1.0
        # big[ nx-16, ny+8 ] += 1.0
        # big[ nx-16, ny+9 ] += 1.0
             
    return big + small


######
##  convenience functions
######

def create_persfile( noise=None,
                     smooth_data='/Users/jberwald/github/local/caja-matematica/pyRBC/data/gauss_peak/gauss_peak.npy' ):
    """
    Convenience function. Sample usage:

    import gaussian as G
    noise = linspace( 0.01, 0.1, 10 )
    for x in noise:
        G.create_persfile( noise=x )

    Saves the perseus-readable (sparse cubical format) to disk (see
    below).
    """
    from pyRBC import rbc_npy2Perseus as rp

    # grab the original file
    A = gauss_bump( noise=noise )

    # find where to clip the noisy surface 
    B = load( smooth_data )
    clip_below( B, 1 ) # in-place, set elements to zero
    w = where( B == 0 )
    A[w] = 0 # now both smooth on noisy surfaces are clipped to zero
             # outside the same boundary.
    
    # scale for additional resolution
    A *= 100

    # might as well save the file for posterity
    noise_level = str( noise )
    # remove the decimal (split on '.', then join the list with '.' removed)
    noise_level = ''.join( noise_level.split( '.' ) )
    sname = './data/gauss_peak/Gnoise/gauss_Gnoise'+noise_level

    # clip the zeros to force a white background in figures
    print "Saving ", sname
    save( sname+'.npy', A )
    rp.write_sparse_file( sname+'.npy',
                          sname+'_pers' )

    
def run_perseus( ):
    """
    Convenience function
    """
    from pyRBC import rbc_perseus as pers

    levels = linspace(0.01,0.1,10)

    persname = '/Users/jberwald/github/local/caja-matematica/pyRBC/data/gauss_peak/Gnoise/gauss_Gnoise'
    for x in levels:
        noise_level = str( x )
        # remove the decimal (split on '.', then join the list with '.' removed)
        noise_level = ''.join( noise_level.split( '.' ) )
        
        fname = persname + noise_level + '_pers.txt'
        outname = persname + noise_level
        print fname
        print outname
        print ""

        pers.perseus( fname, outname )

def make_figures():
    """
    """
    from pyRBC import rbc_postprocess as rpost
    levels = linspace(0.01,0.1,10)

    persname = '/data/jberwald/rbc/gauss/gauss_peak/Gnoise/gauss_Gnoise'
    for x in levels:
        noise_level = str( x )
        # remove the decimal (split on '.', then join the list with '.' removed)
        noise_level = ''.join( noise_level.split( '.' ) )
        fname = persname + noise_level + '_1.txt'
            
        fig = rpost.plot_diagram_std( fname, scale=100, show_fig=False )
        fig.show()
        #fig.savefig( persname + noise_level + '_dia.png', dpi=200 )
    
