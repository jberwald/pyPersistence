//============================================================================
// Name        : WpDistanceDouble.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>
#include "CWpDistance.h"
using namespace std;

int main() {
    CWpDistance d;

    int n_files = 7;
    int B = 0;

    double max_gen = 255;

   /* If you do not want to be working with the dots that live just for a short time you can get rid of them */
    //d.SkipShortGenerators( 100 );
	/* If you do not want to be working with the dots that wher born almost at the end you can get rid of them */
   // d.SkipLastGenerators(254);
	
   double distance = d.Distance( "Out_902001_0.txt", "Out_903001_0.txt", 2, 0);
   std::cout << distance << "\n";

    distance = d.Distance( "Out_902001_0.txt", "Out_962001_0.txt", 2, 0);
    std::cout << distance << "\n";

    distance = d.Distance( "Out_903001_0.txt", "Out_962001_0.txt", 2, 0);
    std::cout << distance << "\n";
    return 0;
}
