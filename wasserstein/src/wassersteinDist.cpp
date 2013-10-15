//============================================================================
// Name        : wassersteinDist.cpp
// Author      : Jesse Berwald (translation of Miro's code)
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>
#include "CWpDistance.hpp"

using namespace std;

int main( int argc, char* argv[]) {

    // must pass in two args, one for each persdia file, so #argc = 1 + 2
    // may also want to pass in max_gen later
    if ( argc < 3 || argc > 4 )
      {
	cout << "\nMust pass in filename1 and filename2" << endl;
	cout << "to find the distance between diagrams." << endl;
	return -1;
      }
    
    // file names to be passed to Distance method 
    char* file1 = argv[1];
    char* file2 = argv[2];

    // Wasserstein p distance. default p=2.
    int p; 
    if ( argc == 4 )
      p = atoi( argv[3] );
    else
      p = 2;

    // Wassterstein distance object
    CWpDistance d;

    int n_files = 2;
    //int B = 0;

    double max_gen = 255;

   /* If you do not want to be working with the dots that live just for a short time you can get rid of them */
   // d.SkipShortGenerators( 40 );
	/* If you do not want to be working with the dots that wher born almost at the end you can get rid of them */
   // d.SkipLastGenerators(254);
	
    double distance = d.Distance( file1, file2, p, max_gen);
    
    cout << distance << endl;

    return 0;
}
