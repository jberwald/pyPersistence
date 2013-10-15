/*
 * CWpDistance.cpp
 *
 *  Created on: Oct 19, 2009
 *      Author: miro
 */

#include <fstream>
#include <math.h>

#include "CMunkres.h"
#include "CWpDistance.h"

using namespace std;

CWpDistance::CWpDistance() {
	NeglectShortGenerators = false;
	NeglectLastGenerators = false;
}

CWpDistance::~CWpDistance() {}

void CWpDistance::LoadGeneratorsFromFile(const char* fileName, std::vector<Generator> &generators, double maxLevel )
{
	Generator gen;
	/* erase generators */
	generators.clear();

	/* Open the file */
	ifstream infile(fileName,  ifstream::in);
	//Test if the file was sucssefuly opened
	if(!infile){
		cout<< " Unable to open input file " << fileName << ". I'll work with an empty persistence diagram! \n";
		return;
	}
	/* Read the generators from the file */
	while(!infile.eof())
	{
		//reads one line of the file
		infile >> gen.birth;
		/* Just in case that files ends in a strange way */
		if( infile.eof() ) break;
		infile >> gen.death;

		//Encorporate Vidits standard that the generator which lives till the end dies at -1
		if( gen.birth == -1 ) gen.birth = maxLevel;
		if( gen.death == -1 ) gen.death = maxLevel;
		//Test if generator should be included (length of life spam plus birth)
		if( fabs(gen.death - gen.birth) <= 0 ) continue;
		if( NeglectShortGenerators && ( fabs(gen.death - gen.birth) <= NeglectSize ) ) continue;
		if( NeglectLastGenerators && ( gen.birth >=  NeglectBornAfter ) ) continue;

		generators.push_back(gen);
	}
	/* Close the file */
	infile.close();
	return;
}
/* Computes distance between two generators L_p */
double  CWpDistance::DistanceOfTwoGenerators(Generator gen1, Generator gen2, int p)
{
	double b = fabs( gen1.birth - gen2.birth );
	double d = fabs( gen1.death - gen2.death );

	double max;
	if (b > d) max = b;
	else max = d;

	if(p == 1 ) return max;
	else return  pow(max, p);
}

/* Computes L_p distance of the generator from the diagonal */
double CWpDistance::DistanceOfGeneratorFromDiagonal(Generator gen, int p)
{
	double d = ( fabs(gen.death - gen.birth) ) / 2;
	if( p == 1 ) return d;
	else return  pow( d , p);
}

/* Computes distaves between the persistence diagrams contained in Generators1 and Generatoros2 */
double CWpDistance::ComputeDistance( int p )
{
	/* Distance matrix  the generators in Generators1 and Generators2 */
	double*	distanceMatrix;
	/* size of the distance matrix */
	unsigned int 	matrixSize;

	/*Distance matrix has max(Generators1.size(), Generators2.size())^2 elements */
	if( Generators1.size() > Generators2.size() ) matrixSize = Generators1.size();
	else matrixSize = Generators2.size();
	/*Allocate the matrix */
	distanceMatrix = new double[matrixSize * matrixSize];
	/* if both persistence diagrams are empty than their distance is zero */
	if ( !matrixSize ) return 0;

	/*Prepare distance matrix (if there is different number of generators, then we add extra rows (columns)
	  with distance of the generator from the diagonal */
	for( unsigned int  i = 0; i < matrixSize; ++ i )
		for( unsigned int j = 0; j < matrixSize; ++ j ){
			if( i >= Generators1.size()){
				distanceMatrix[ i * matrixSize + j ] = DistanceOfGeneratorFromDiagonal( Generators2[ j ], p );
			}
			else if (j >=  Generators2.size() ){
				distanceMatrix[ i * matrixSize + j ] = DistanceOfGeneratorFromDiagonal( Generators1[ i ], p );
				if( distanceMatrix[ i * matrixSize + j ] < 0 ) std::cout << " Ups!\n";
			}
			else{
				distanceMatrix[ i * matrixSize + j ] = DistanceOfTwoGenerators( Generators1[ i ], Generators2[ j ], p );
			}
		}

	/* Class with Munkres algorithm for computing minimal price of the matrix */
	CMunkres munkres;
	double distance;
	/* Compute the minimal price of the matrix. */
	munkres.GetPrice(distanceMatrix, matrixSize, distance);

	/* Matrix not needed any more. Free the memory */
	delete[] distanceMatrix;

	if( p == 1) return distance;
	if ( p == 2 ) return sqrt((double) ( distance ));
	return pow( distance, (double) (1.0 /(double)(p) ) );

}

double CWpDistance::Distance( const char* genFile1, const char* genFile2, int p, double maxLevel ){
	LoadGeneratorsFromFile( genFile1,  Generators1,  maxLevel );
	LoadGeneratorsFromFile( genFile2,  Generators2,  maxLevel );
	return ComputeDistance( p );
}

void CWpDistance::ResetSettings()
{
	NeglectShortGenerators = false;
	NeglectLastGenerators = false;
}

void CWpDistance::SkipShortGenerators(double size)
{
	NeglectShortGenerators = true;
	NeglectSize = size;

}

void CWpDistance::SkipLastGenerators(double bornAfter)
{
	NeglectLastGenerators = true;
	NeglectBornAfter = bornAfter;
}
