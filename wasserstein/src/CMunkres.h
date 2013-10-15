/*
 * CMunkres.h
 *
 *  Created on: Oct 15, 2009
 *      Author: miro
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#ifndef CMUNKRES_H_
#define CMUNKRES_H_

class CMunkres {
private:
	int		size;     /* size of the matrix */
	double		*matrix;  /* Copy of the matrix which is going to be minimized */
	int			*mask;    /* minimization mask */
	int		*cRow;    /* covered rows */
	int		*cCol;    /*cover coluns*/
	int		*rPath;   /*row path*/
	int		*cPath;   /*column path */

	void ClearMemory();
	void SetVariablesAndPrepareMemory(double* Matrix, int Size);

	void munkresS1(int &NextStep);
	void munkresS2(int &NextStep);
	void munkresS3(int &NextStep);
	void munkresS4(int &NextStep);
	void munkresS5(int &NextStep);
	void munkresS6(int &NextStep);

	void findZero(int &row, int &col);
	bool starInRaw(int row);
	void findStarInRow(int row, int &col);
	void findStarInCol(int col, int &row);
	void findPrimeInRow(int row, int &col);
	void convertPath(int count);
	void clearCovers();
	void erasePrimes();
	double findSmallest();



public:
	CMunkres();
	virtual ~CMunkres();
	bool GetPrice(double *matrix, int size, double &price);
};

#endif /* CMUNKRES_H_ */
