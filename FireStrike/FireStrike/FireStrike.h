#pragma once
#include <iostream>
#include <list>
#include <vector>
#include <random>
#include "Parameter.h"
#include "ShootTable.h"

using namespace std;

class _declspec(dllexport) FireStrike
{
private:
	int m_nSeed = 0;
	list<ShootTable> m_tables;
public:
	FireStrike();
	~FireStrike();

	virtual vector<double> getFiringDeviation(ShootTable table, float distance, vector<double> mu);
	virtual vector<double> getFiringDeviation(int weaponId, float distance, vector<double> mu);
	virtual vector<double> getFiringDeviation(vector<double> sigma, vector<double> mu);

	virtual void setSeed(int seed);

	virtual void insertShootTable(string json);
	virtual void insertShootTable(ShootTable table);

	virtual ShootTable getShootTable(int id);
	virtual list<ShootTable> getShootTables();
};

