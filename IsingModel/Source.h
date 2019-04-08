#pragma once
#include <math.h>
#include <stdlib.h>
#include <random>


double random();

class State
{
public:
	State(unsigned int par_L, double par_T);
	~State();
	void mcStep();
	double magnetization();
	char getSpin(unsigned int i, unsigned int j);
	int getSize();
private:
	unsigned int L; //rozmiar uk³adu
	char** state_array;
	double T;	//temp. zredukowana
	double w_values[5];
	inline double w(char dU);
	
};