/*
 * CMunkres.cpp
 *
 *  Created on: Oct 15, 2009
 *      Author: miro
 */

#include "CMunkres.h"
#include <iostream>

using namespace std;

CMunkres::CMunkres() {
	matrix = NULL;
	mask  = NULL;
	cRow = NULL;
	cCol = NULL;
	rPath = NULL;
	cPath = NULL;
}

CMunkres::~CMunkres() {
	ClearMemory();
}

void CMunkres::ClearMemory()
{
	if(matrix != NULL) delete[] matrix;
	if(mask  != NULL) delete[] mask;
	if(cRow != NULL) delete[] cRow;
	if(cCol != NULL) delete[] cCol;
	if(rPath != NULL) delete[] rPath;
	if(cPath != NULL) delete[] cPath;

	matrix = NULL;
	mask  = NULL;
	cRow = NULL;
	cCol = NULL;
	rPath = NULL;
	cPath = NULL;
}

/*
 * Makes a copy of the Matrix to matrix and alocates
 * memory for the structures needed to compute the minimal price
 */
void CMunkres::SetVariablesAndPrepareMemory(double* Matrix, int Size)
{
	size = Size;
	ClearMemory();

	matrix = new double[size * size];
	memcpy( matrix, Matrix, size * size * sizeof(double));

	cRow = new int[size];
	cCol = new int[size];
	memset(cCol, 0, size * sizeof(int));
	memset(cRow, 0, size * sizeof(int));

	rPath = new int[2 * size];
	cPath = new int[2 * size];

	mask = new int[size * size];
	memset(mask, 0, size * size * sizeof(int));

}

/*
 * Computes a minimal price for the given square matrix with dimension size * size
 */
bool CMunkres::GetPrice(double *Matrix, int Size, double &Price)
{

	bool	done = false;
	int		step = 1;

	int i,j;

	SetVariablesAndPrepareMemory(Matrix, Size);

	while(!done)
	{
		switch(step)
		{
		case 1:
			munkresS1(step);
			break;
		case 2:
			munkresS2(step);
			break;
		case 3:
			munkresS3(step);
			break;
		case 4:
			munkresS4(step);
			break;
		case 5:
			munkresS5(step);
			break;
		case 6:
			munkresS6(step);
			break;
		default:
			done = true;
			break;
		}
	}

	Price = 0;
	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
			if(mask[i * size + j] == 1)
			{
				Price += Matrix[i * size + j];
			}


	ClearMemory();
	return true;

}



/*
 * Six sub steps of Munkres algorithm
 */

void CMunkres::munkresS1(int &NextStep)
{
	int i,j;
	double minVal;

	for(i = 0; i < size; i++)
	{
		minVal = matrix[i * size];
		for(j = 0; j < size; j++)
			if(minVal > matrix[i * size + j])
				minVal = matrix[i * size + j];

		for(j = 0; j < size; j++)
			matrix[i * size + j] = matrix[i * size + j] - minVal;
	}
	NextStep = 2;
}

void CMunkres::munkresS2(int &NextStep)
{
	int i,j;

	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
			if(matrix[i*size + j] == 0 && cCol[j] == 0 && cRow[i] == 0)
			{
				mask[i*size + j] = 1;
				cCol[j] = 1;
				cRow[i] = 1;
			}

	memset(cCol, 0, size * sizeof(int));
	memset(cRow, 0, size * sizeof(int));

	NextStep = 3;

}

void CMunkres::munkresS3(int &NextStep)
{
	int count = 0;
	int i,j;

	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
			if(mask[i*size + j] == 1)
				cCol[j] = 1;

	for(j = 0; j < size; j++)
		count += cCol[j];

	if(count >= size)
		NextStep = 7;
	else
		NextStep = 4;

}

void CMunkres::findZero(int &row, int &col)
{
	int i,j;
	bool done = false;

	row = -1;
	col = -1;

	i = 0;
	do
	{
		j = 0;
		do{
			if(matrix[i*size + j] == 0 && cCol[j] == 0 && cRow[i] == 0)
			{
				row = i;
				col = j;
				done = true;
			}
			j++;
		}while(j < size);

		i++;
		if(i >= size)
			done = true;

	}while(!done);

}

bool CMunkres::starInRaw(int row)
{
	int j;
	bool tbool = false;

	for(j = 0; j < size; j++)
		if(mask[row * size + j] == 1)
			tbool = true;

	return tbool;
}

void CMunkres::findStarInRow(int row, int &col)
{
	int j;

	col = -1;

	for(j = 0; j < size; j++)
		if(mask[row * size + j] == 1)
			col = j;
}

void CMunkres::munkresS4(int &NextStep)
{
	int row,col;
	bool done = false;

	while(!done)
	{
		findZero(row, col);
		if(row == -1)
		{
			done = true;
			NextStep = 6;
		}
		else
		{
			mask[row*size + col] = 2;
			if( starInRaw(row) )
			{
				findStarInRow(row, col);
				cRow[row] = 1;
				cCol[col] = 0;
			}
			else
			{
				done = true;
				NextStep = 5;
				rPath[0] = row;
				cPath[0] = col;

			}
		}
	}
}

void CMunkres::findStarInCol(int col, int &row)
{
	int i;

	row = -1;

	for(i = 0; i < size; i++)
		if(mask[i * size + col] == 1)
			row = i;
}

void CMunkres::findPrimeInRow(int row, int &col)
{
	int j;

	col = -1;

	for(j = 0; j < size; j++)
		if(mask[row * size + j] == 2)
			col = j;
}

void CMunkres::convertPath(int count)
{
	int i;

	for(i = 0; i < count; i++)
	{
		if(mask[rPath[i] * size + cPath[i]] == 1)
			mask[rPath[i] * size + cPath[i]] = 0;
		else
			mask[rPath[i] * size + cPath[i]] = 1;
	}
}

void CMunkres::clearCovers()
{
	memset(cRow, 0, size * sizeof(int));
	memset(cCol, 0, size * sizeof(int));
}

void CMunkres::erasePrimes()
{
	int i,j;
	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
			if(mask[i * size + j] == 2)
				mask[i * size + j] = 0;

}

void CMunkres::munkresS5(int &NextStep)
{
	int row, col;
	int count = 1;
	bool done = false;

	while(!done)
	{
		findStarInCol(cPath[count -1], row);
		if(row >= 0)
		{
			count++;
			rPath[count - 1] = row;
			cPath[count - 1] = cPath[count - 2];
		}
		else
		{
			done = true;
		}

		if(!done)
		{
			findPrimeInRow(rPath[count -1], col);
			count++;
			rPath[count -1] = rPath[count - 2];
			cPath[count -1] = col;
		}
	}

	convertPath(count);
	clearCovers();
	erasePrimes();

	NextStep = 3;
}

double CMunkres::findSmallest()
{
	int i,j;
	double minVal = 0;
	bool first = true;

	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
			if(cRow[i] == 0 && cCol[j] == 0)
				if(matrix[i * size + j] < minVal || first)
				{
					minVal = matrix[i * size + j];
					first = false;
				}
	return minVal;

}

void CMunkres::munkresS6(int &NextStep)
{
	int i,j;
	double minVal;

	minVal = findSmallest();

	for(i = 0; i < size; i++)
		for(j = 0; j < size; j++)
		{
			if(cRow[i] == 1)
				matrix[i * size + j] = matrix[i * size + j] + minVal;
			if(cCol[j] == 0)
				matrix[i * size + j] = matrix[i * size + j] - minVal;
		}

	NextStep = 4;
}


