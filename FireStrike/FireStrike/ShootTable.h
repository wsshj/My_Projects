#pragma once
#include <iostream>
#include <list>
#include "Parameter.h"

using namespace std;

class _declspec(dllexport) ShootTable
{
public:
	int m_nId = 0;
	string m_strName = "";
	float m_fBulletWeight = 0;
	int m_nInitialSpeed = 0;
	list<Parameter> m_Parameters;

	ShootTable();
	ShootTable(int id, string name);

	ShootTable(int id, string name, float bulletWeight, int initialSpeed);

	void addParameters(Parameter parameter);

	~ShootTable();
};

