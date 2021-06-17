#include "pch.h"
#include "ShootTable.h"

ShootTable::ShootTable()
{
}

ShootTable::ShootTable(int id, string name)
{
	m_nId = id;
	m_strName = name;
	m_Parameters.clear();
}

ShootTable::ShootTable(int id, string name, float bulletWeight, int initialSpeed)
{
	m_nId = id;
	m_strName = name;
	m_fBulletWeight = bulletWeight;
	m_nInitialSpeed = initialSpeed;
	m_Parameters.clear();
}

ShootTable::~ShootTable()
{
}


void ShootTable::addParameters(Parameter parameter)
{
	m_Parameters.push_back(parameter);
}

