/*
 * 2dim.hpp
 * Cell Complex Examples for 2 dimensional manifolds
 * This code is unreadable.
 */

#ifndef DIM2_HPP_
#define DIM2_HPP_

#include "../Cells/All.h"
#include "../Complexes/All.h"
#include "../Algos/All.h"


template <typename C, typename PS>
SToplex<C,PS>* stopRtTrgs_2D()
{
	Point<PS>* mypt1 = new Point<PS>;
	mypt1->push(0); mypt1->push(0); // pt1 = (0,0)
	Point<PS>* mypt2 = new Point<PS>;
	mypt2->push(0); mypt2->push(1); // pt2 = (0,1)
	Point<PS>* mypt3 = new Point<PS>;
	mypt3->push(1); mypt3->push(0); // pt3 = (1,0)
	Point<PS>* mypt4 = new Point<PS>;
	mypt4->push(2); mypt4->push(0); // pt4 = (2,0)
	Point<PS>* mypt5 = new Point<PS>;
	mypt5->push(1); mypt5->push(1); // pt5 = (1,1)
	Point<PS>* mypt6 = new Point<PS>;
	mypt6->push(0); mypt6->push(2); // pt6 = (1,2)
	Point<PS>* mypt7 = new Point<PS>;
	mypt7->push(2); mypt7->push(1); // pt7 = (2,1)


	PT_SET myptset;
	myptset.insert(mypt1);
	myptset.insert(mypt2);
	myptset.insert(mypt3);

	Simplex<C,PS>* mysimp1 = new Simplex<C,PS>(myptset);

	myptset.clear();
	myptset.insert(mypt2);
	myptset.insert(mypt5);
	myptset.insert(mypt6);

	Simplex<C,PS>* mysimp2 = new Simplex<C,PS>(myptset);

	myptset.clear();
	myptset.insert(mypt3);
	myptset.insert(mypt5);
	myptset.insert(mypt4);

	Simplex<C,PS>* mysimp3 = new Simplex<C,PS>(myptset);

	myptset.clear();
	myptset.insert(mypt1);
	myptset.insert(mypt2);
	myptset.insert(mypt7);

	Simplex<C,PS>* mysimp4 = new Simplex<C,PS>(myptset);

	vector<Simplex<C,PS>*> topsvec;
	topsvec.push_back(mysimp1);
	topsvec.push_back(mysimp2);
	topsvec.push_back(mysimp3);
	topsvec.push_back(mysimp4);
	SToplex<C,PS>* toret = new SToplex<C,PS>;

	toret->populateMap(topsvec);
	return toret;
}


// a simple cubical figure-8, relies on cubical toplex information
template <typename C, typename PS>
CToplex<C,PS>* ctopFig8_2D(bool makeb = true)
{
	vector<Point<PS>*> ancs;
	Point<PS>* curpt;

	// we just add the 18 (!!) anchors

	curpt = new Point<PS>();
	curpt->push(0); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-1); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-2); curpt->push(-1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-3); curpt->push(-1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-4); curpt->push(-1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-4); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-4); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-3); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-2); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(-2); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(1); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(1); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(2); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(3); curpt->push(1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(3); curpt->push(0);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(3); curpt->push(-1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(2); curpt->push(-1);
	ancs.push_back(curpt);

	curpt = new Point<PS>();
	curpt->push(1); curpt->push(-1);
	ancs.push_back(curpt);

	CToplex<C,PS>* fig8 = new CToplex<C,PS>();

	vector<int>* births = NULL;
	if (makeb)
	{
		births = new vector<int>;
		for (unsigned int i = 0; i < ancs.size(); ++i)
		{
			births->push_back(i%2 + 1); // fill with 1 or 2...
		}
	}


	fig8->buildTopCubeMap(2,ancs, births);
	delete births;
	fig8->addCubeFaces();

	return fig8;
}

// generates a cubical torus
template <typename C>
MComplex<C>* cubTorus_2D()
{
	MComplex<C>* torus = new MComplex<C>;
	if(EGTALK) {cout<<"\n making torus..."; cin.get();}

	vector<Cell<C>*> zerocells;
	for (int i=0; i<9; i++)
	{
		zerocells.push_back(new Cell<C>(0,i));
		torus->insertCell(zerocells[i]);
	}

	if(EGTALK) {cout<<"\n     0 cells..."; cin.get();}

	vector<Cell<C>*> onecells;
	for (int i=0; i<18; i++)
	{
		onecells.push_back(new Cell<C>(1,i));
		torus->insertCell(onecells[i]);
	}

	if(EGTALK) {cout<<"\n     1 cells...";}

	// and now boundaries, UGH!
	int modn=0;
	// horizontal...
	for(int i=0; i<9; i++)
	{
		if (i%3 == 0) modn+=3;

		onecells[i]->addBDLink(zerocells[i%modn],-1);
		if (i%3 != 2)onecells[i]->addBDLink(zerocells[(i+1)%modn],1);
		else onecells[i]->addBDLink(zerocells[i-2],1);
	}

	if(EGTALK) {cout<<" + h-bds";}

	// and now vertical...
	modn = -1;
	for(int i=0; i<9; i++)
	{
		if (i%3==0) modn++;

		onecells[i+9]->addBDLink(zerocells[modn+(3*i)%9],-1);
		onecells[i+9]->addBDLink(zerocells[modn+(3*i+3)%9],1);
	}

	if(EGTALK) {cout<<" + v-bds\n    2 - cells"; cin.get();}

	Cell<C>* cur;
	modn = 0;
	// two-cells too!
	vector<Cell<C>*> twocells;
	for (int i=0; i<9; i++)
	{
		cur = new Cell<C>(2,i);
		twocells.push_back(cur);
		cur->birth = (i % 2) == 0 ? 0 : 1;
		//cur->birth = 1;
		torus->insertCell(cur);

		// up-down faces
		cur->addBDLink(onecells[i],-1);
		cur->addBDLink(onecells[(i+3)%9],1);

		// left-right faces
		modn = i/3 + 3*(i%3)+9;

		cur->addBDLink(onecells[modn],-1);
		cur->addBDLink(onecells[(i%3==2) ? modn-6:(modn+3)%18],1);
	}
	return torus;
}

// generates a cubical klein bottle
// ***************************************************************TO BE WRITTEN!
template <typename C, typename BT>
MComplex<C,BT>* cubKleinBot_2D()
{
	MComplex<C,BT>* kleinbot = new MComplex<C,BT>;

	if(EGTALK) {cout<<"\n making klein bottle...";}

	vector<Cell<C,BT>*> zerocells;
	for (int i=0; i<9; i++)
	{
		zerocells.push_back(new Cell<C,BT>(0,i));
		kleinbot->insertCell(zerocells[i]);
	}

	if(EGTALK) {cout<<"\n     0 cells...";}

	vector<Cell<C,BT>*> onecells;
	for (int i=0; i<18; i++)
	{
		onecells.push_back(new Cell<C>(1,i));
		kleinbot->insertCell(onecells[i]);
	}

	if(EGTALK) {cout<<"\n     1 cells...";}

	// and now boundaries, UGH!
	CCHAIN curbd;
	int modn=0;
	// horizontal...
	for(int i=0; i<9; i++)
	{
		if (i%3 == 0) modn+=3;
		curbd.cells.clear();

		curbd.addLink(zerocells[i],-1);
		// for 5 and 8... flip torus links
		if (i==5)
		{
			curbd.addLink(zerocells[6],1);
		}
		else if(i==8)
		{
			curbd.addLink(zerocells[3],1);
		}
		else
		{
			curbd.addLink(zerocells[(i+1)%modn],1);
		}
		onecells[i]->setBD(curbd);
	}

	if(EGTALK) {cout<<" + h-bds";}

	// and now vertical...
	modn = -1;
	for(int i=0; i<9; i++)
	{
		if (i%3==0) modn++;
		curbd.cells.clear();
		//if (EGTALK) {cout<<endl<<i<<" "<<modn<<" "<<modn+(3*i)%9; cin.get();}

		curbd.addLink(zerocells[modn+(3*i)%9],-1);
		curbd.addLink(zerocells[modn+(3*i+3)%9],1);
		onecells[i+9]->setBD(curbd);
		//if (EGTALK) {cout<<"D("<<*onecells[i+9]<<") = "<<curbd; cin.get();}
	}

	if(EGTALK) {cout<<" + v-bds\n    2 - cells"; }

	modn = 0;
	// two-cells too!
	vector<Cell<C,BT>*> twocells;
	for (int i=0; i<9; i++)
	{
		twocells.push_back(new Cell<C>(2,i));
		kleinbot->insertCell(twocells[i]);
		curbd.cells.clear();

		//up-down faces
		curbd.addLink(onecells[i],-1);
		curbd.addLink(onecells[(i+3)%9],1);

		modn = i/3 + 3*(i%3)+9;

		// left-right faces
		curbd.addLink(onecells[modn],-1);
		if (i%3 == 2) curbd.addLink(onecells[11 - i/3],-1);
		else curbd.addLink(onecells[(i%3==2) ? modn-6:(modn+3)%18],1);

		twocells[i]->setBD(curbd);

	}
	return kleinbot;
}


// generates sphere S2
template <typename C, typename PS>
MComplex<C>* cubSphere_2D()
{
	MComplex<C>* toret = NULL;
	return toret;
}


// Generates RP^2
template <typename C, typename BT>
MComplex<C,BT>* cubRProj_2D()
{
	MComplex<C,BT>* rproj = new MComplex<C,BT>;

	if(EGTALK) {cout<<"\n making RP^2...";}

	vector<Cell<C,BT>*> zerocells;
	for (int i=0; i<9; i++)
	{
		zerocells.push_back(new Cell<C,BT>(0,i));
		rproj->insertCell(zerocells[i]);
	}

	vector<Cell<C,BT>*> onecells;
	for (int i=0; i<18; i++)
	{
		onecells.push_back(new Cell<C,BT>(1,i));
		rproj->insertCell(onecells[i]);
	}

	if(EGTALK) {cout<<"\n     1 cells...";}

	// and now boundaries, UGH!
	CCHAIN curbd;
	int modn=0;
	// horizontal...
	for(int i=0; i<9; i++)
	{
		if (i%3 == 0) modn+=3;
		curbd.cells.clear();

		curbd.addLink(zerocells[i],-1);
		// for 5 and 8... flip torus links
		switch(i)
		{
		case 5:
			curbd.addLink(zerocells[6],1);
			break;
		case 8:	curbd.addLink(zerocells[3],1);
			break;
		default: curbd.addLink(zerocells[(i+1)%modn],1);
		}
		onecells[i]->setBD(curbd);
	}


	// and now vertical...
	modn = -1;
	for(int i=0; i<9; i++)
	{
		if (i%3==0) modn++;
		curbd.cells.clear();

		curbd.addLink(zerocells[modn+(3*i)%9],-1);

		// exceptions: the twist
		switch(i)
		{
		case 5:
			curbd.addLink(zerocells[2],1);
			break;
		case 8:
			curbd.addLink(zerocells[1],1);
			break;
		default: curbd.addLink(zerocells[modn+(3*i+3)%9],1);
		}
		onecells[i+9]->setBD(curbd);
		//if (EGTALK) {cout<<"D("<<*onecells[i+9]<<") = "<<curbd; cin.get();}
	}

	if(EGTALK) {cout<<" + v-bds\n    2 - cells"; }

	modn = 0;
	// two-cells too!
	vector<Cell<C>*> twocells;
	for (int i=0; i<9; i++)
	{
		twocells.push_back(new Cell<C>(2,i));
		rproj->insertCell(twocells[i]);
		curbd.cells.clear();

		//up-down faces

		curbd.addLink(onecells[i],-1);
		if (i<6) curbd.addLink(onecells[i+3],1);
		else curbd.addLink(onecells[8-i],-1);

		// left-right faces
		modn = i/3 + 3*(i%3)+9;

		curbd.addLink(onecells[modn],-1);
		if (i%3 == 2) curbd.addLink(onecells[26 - modn],-1);
		else curbd.addLink(onecells[(modn+3)%18],1);


		twocells[i]->setBD(curbd);

	}
	return rproj;
}


template <typename C, typename BT>
MComplex<C,BT>* cubMrozek_2D()
{
	MComplex<C,BT>* toret = new MComplex<C>;

	vector<Cell<C,BT>*> zeros, twos;

	// fill up zero cells
	for (int i=0; i<35; i++)
	{
		zeros.push_back(new Cell<C>(0,i));
		toret->insertCell(zeros.at(i));
	}

	// one cells...

	// first all connections to the god point
	Cell<C,BT>* gpcon; // god point connector
	CCHAIN gbd;
	for (int i=1; i<35; i++)
	{
		gpcon = new Cell<C>(1,i);

		gbd.cells.clear();
		gbd.addLink(zeros.at(0),-1);
		gbd.addLink(zeros.at(i),1);

		gpcon->setBD(gbd);

		toret->insertCell(gpcon);
	}

	//cout<<*toret;
	return toret;

}


#endif /* DIM2_HPP_ */
