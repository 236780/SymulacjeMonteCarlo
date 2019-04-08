#include "Source.h"

double random()
{
	static std::default_random_engine e;
	static std::uniform_real_distribution<> dis(0, 1);
	return dis(e);
}

State::State(unsigned int par_L, double par_T)
{
	L = par_L;
	T = par_T;

	//Alokacja tablicy L*L
	state_array = (char**)malloc(L * sizeof(char*));
	for (unsigned int i = 0; i < L; i++)
		state_array[i] = (char*)malloc(L * sizeof(char));


	//Wyznaczenie wartoœci w(T) dla mo¿liwych dU
	w_values[0] = exp(+8.0 / T); //dU=-8
	w_values[1] = exp(+4.0 / T); //dU=-4
	w_values[2] = exp(0 / T);    //dU=0
	w_values[3] = exp(-4.0 / T); //dU=4
	w_values[4] = exp(-8.0 / T); //dU=8

	//Wylosowanie konfiguracji pocz¹tkowej
	for (unsigned int i = 0; i < L; i++)
	for (unsigned int j = 0; j < L; j++)
	{
		state_array[i][j] =
			(random() >= 0.5) ? +1 : -1;
	}

}

State::~State()
{
	//Zwolnienie tablicy L*L
	for (unsigned int i = 0; i < L; i++)
		free(state_array[i]);
	free(state_array);
}

void State::mcStep()
{

	for (unsigned int i = 0; i < L; i++)
	for (unsigned int j = 0; j < L; j++)
	{
		char dU = 2 * state_array[i][j] *
			(state_array[(i - 1) % L][j] + state_array[(i + 1) % L][j] +
				state_array[i][(j - 1) % L] + state_array[i][(j + 1) % L]);
		if (dU <= 0 || random()<=w(dU))
			state_array[i][j] = -state_array[i][j];
	}
}

double State::magnetization()
{
	int m = 0;
	for (unsigned int i = 0; i < L; i++)
	for (unsigned int j = 0; j < L; j++)
	{
		m += state_array[i][j];
	}
	double magnetization = (double)m / (L*L);
	return m;
}

char State::getSpin(unsigned int i, unsigned int j)
{
	return state_array[i][j];
}

inline double State::w(char dU)
{
	return w_values[(dU+8)/4];
}

int State::getSize()
{
	return L;
}

std::string State::getMatrix()
{
	std::string output = "";
	for (unsigned int i = 0; i < L; i++)
	{
		for (unsigned int j = 0; j < L; j++)
		{
			output += std::to_string(state_array[i][j]);
			output += " ";
		}
		output += "\n";
	}
	return output;
}
