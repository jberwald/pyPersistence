pyPersistence
=============

Collection of modules for handling persistent topology computations on data. 

Requirements:
------------

Python 2.7
matplotlib 1.0 +
numpy 1.5 +

Perseus (http://www.math.rutgers.edu/~vidit/perseus/index.html)

Wasserstein distance code (provided)
Bottleneck distance code (provided)

Running build_lib.sh should compile and test both for functionality. 

If somethign goes wrong: See README in distance folders for compilation instructions. You may have to alter the compiler flags (tested only on Linux and Mac).

Once compiled, the names 'wasserstein' and 'bottleneck' can be found in wasserstein/src and bottleneck/src, respectively. Both of these are executable and must be in your PATH. 
