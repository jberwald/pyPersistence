/*
 * 1dim.hpp
 *
 *  Created on: Jun 17, 2010
 *      Author: administrtor
 */

#ifndef DIM1_HPP_
#define DIM1_HPP_

# include "../Complexes/All.h"

template <typename C, typename BT>
MComplex<C,BT>* cubCircle_1D(bool fill = false)
{
	// 4 points...
	Cell<C,BT>* a = new Cell<C,BT>(0,0);
	Cell<C,BT>* b = new Cell<C,BT>(0,1);
	Cell<C,BT>* c = new Cell<C,BT>(0,2);
	Cell<C,BT>* d = new Cell<C,BT>(0,3);

	a->birth=1;b->birth=1;c->birth=1;d->birth=1;

	// 4 lines...
	Cell<C,BT>* ab = new Cell<C,BT>(1,0);
	Cell<C,BT>* ac = new Cell<C,BT>(1,1);
	Cell<C,BT>* bd = new Cell<C,BT>(1,2);
	Cell<C,BT>* cd = new Cell<C,BT>(1,3);

	ab->birth=1;ac->birth=1;bd->birth=1;cd->birth=2;
	// and the boundary relations!
	map<Cell<C,BT>*,C > bdchain;
	bdchain[b]=1;
	bdchain[a]=-1;
// one
	ab->setBD(bdchain);

	bdchain.clear();
	bdchain[c]=1;
	bdchain[a]=-1;

// two
	ac->setBD(bdchain);

	bdchain.clear();
	bdchain[d] = 1;
	bdchain[b] = -1;
// three
	bd->setBD(bdchain);

	bdchain.clear();
	bdchain[d] = 1;
	bdchain[c] = -1;
// four!
	cd->setBD(bdchain);

	MComplex<C,BT>* mycomp = new MComplex<C,BT>;
	mycomp->insertCell(a);
	mycomp->insertCell(b);
	mycomp->insertCell(c);
	mycomp->insertCell(d);

	mycomp->insertCell(ab);
	mycomp->insertCell(ac);
	mycomp->insertCell(bd);
	mycomp->insertCell(cd);

	if (fill)
	{

		Cell<C,BT>* abcd = new Cell<C,BT>(2,0);
		bdchain.clear();

		bdchain[ab] =  1;
		bdchain[ac] =  1;
		bdchain[cd] =  -1;
		bdchain[bd] =  -1;

		abcd->setBD(bdchain);
		abcd->birth = 4;
		mycomp->insertCell(abcd);
	}


	return mycomp;
}

#endif /* 1DIM_HPP_ */
