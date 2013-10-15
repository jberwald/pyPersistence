/*
 * CWpDistance.h
 *
 *  Created on: Oct 19, 2009
 *      Author: miro
 */

#ifndef CWPDISTANCE_H_
#define CWPDISTANCE_H_

#include <iostream>
#include <vector>

class Generator{
public:
	double birth;
	double death;

};

class CWpDistance {

private:
	/* generators for two persistence diagrams which are going to be compared */
	std::vector<Generator> Generators1;
	std::vector<Generator> Generators2;

	bool NeglectShortGenerators;
	bool NeglectLastGenerators;

	double  NeglectSize;
	double  NeglectBornAfter;

	/* Loads generators from the file */
	void LoadGeneratorsFromFile(const char* fileName, std::vector<Generator> &generators, double maxLevel );
	/* Computes distance between two generators */
	double  DistanceOfTwoGenerators(Generator gen1, Generator gen2, int p);
	/* Computes distance from the diagonal for the given generator */
	double DistanceOfGeneratorFromDiagonal(Generator gen, int p);

	/* Computes the p-Wasserstein distance  between the persistence diagrams with generators stored in
	 * Generatores1 and Generators2 */
	double ComputeDistance( int p );


public:
	CWpDistance();
	virtual ~CWpDistance();

	/* Computes p-Wasserstain distance between tow persistence diagrams  with generators stored in
	 * the files genFile1 and genFile2
	 * MaxLevel is the maximal level till Vidit's persistence algorithm goes.
	 * I replace the -1 entry ( for the generator which does not die by the MaxLevel )
	 */
	double Distance(const char* genFile1, const char* genFile2, int p, double maxLevel);

	/* Resets to default settings. It all generators are taken in account */
	void ResetSettings();
	/* Neglect the generators with live span shorter than size */
	void SkipShortGenerators(double size);
	/* Neglect generators born after bornAfter */
	void SkipLastGenerators(double bornAfter);
};

#endif /* CWPDISTANCE_H_ */
