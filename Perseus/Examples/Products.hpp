/*
 * Products.hpp
 *
 * */

#ifndef PRODUCTS_HPP_
#define PRODUCTS_HPP_

# include "../DebugV.h"
# include "../Complexes/Complex.hpp"

// returns the product of two complexes
template <typename C,typename BT>
Complex<C,BT>* makeProduct(Complex<C,BT>& c1, Complex<C,BT>& c2)
{
	Complex<C,BT>* prod = new Complex<C,BT>(c1.topdim*c2.topdim);
	typename COMPLEX::iterator cell1, cell2;
	Cell<C>* toins;

	// loop over every possible dimension
	for (int i=0; i <= c1.topdim; i++)
	{
		for (int j=0; i <= c2.topdim; j++)
		{
			// and now iterate through the cells of these dimensions (i,j)
			for (cell1 = c1.begin(i); cell1 != c1.end(i); ++cell1)
			{
				for (cell2 = c2.begin(j); cell2 != c2.end(j); ++cell2)
				{
					toins = new Cell<C,BT>;
					prod->insertCell(i+j, toins);
					// gotta make coboundary or boundary!
				}
			}
		}

	}

}



#endif /* PRODUCTS_HPP_ */
