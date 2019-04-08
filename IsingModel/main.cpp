#include <stdio.h>
#include <iostream>
#include "Source.h"

double T = 1.7;
long long steps = 1000000;
long long skip_first = 0;
long long take_every = 1000;
unsigned int L = 12; //rozmiar uk�adu

int main()
{

	State state = State(L,T);
	for (long long i = 0; i < steps; i++)
	{
		if (i >= skip_first && i % take_every == 0)
		{
			std::cout <<i<<"\t" << state.magnetization()<<std::endl; 
		}

		state.mcStep();
	}
}