#include "pch.h"
#include "FireStrike.h"

FireStrike::FireStrike()
{
}

FireStrike::~FireStrike()
{
}

vector<double> FireStrike::getFiringDeviation(ShootTable table, float distance, vector<double> mu)
{
	static default_random_engine e(m_nSeed == 0 ? time(0) : m_nSeed); //引擎

	if (mu.size() < 2)
	{
		return mu;
	}

	float sigma_x = 1;
	float sigma_y = 1;

	list<Parameter>::iterator itor;
	for (itor = table.m_Parameters.begin(); itor != table.m_Parameters.end(); itor++)
	{
		Parameter para = *itor;
		if (para.m_distance / 100 == round(distance / 100))
		{
			sigma_x = para.m_spreadx;
			sigma_y = para.m_spready;
		}
	}

	normal_distribution<double> n_x(mu[0], sigma_x); //均值, 方差
	normal_distribution<double> n_y(mu[1], sigma_y); //均值, 方差

	vector<double> Offset;

	Offset.push_back(n_x(e));
	Offset.push_back(n_y(e));

	return Offset;
}

vector<double> FireStrike::getFiringDeviation(int weaponId, float distance, vector<double> mu)
{
	static default_random_engine e(m_nSeed == 0 ? time(0) : m_nSeed); //引擎

	if (mu.size() < 2)
	{
		return mu;
	}

	float sigma_x = 1;
	float sigma_y = 1;

	ShootTable table = getShootTable(weaponId);

	list<Parameter>::iterator itor;
	for (itor = table.m_Parameters.begin(); itor != table.m_Parameters.end(); itor++)
	{
		Parameter para = *itor;
		if (para.m_distance / 100 == round(distance / 100))
		{
			sigma_x = para.m_spreadx;
			sigma_y = para.m_spready;
		}
	}

	normal_distribution<double> n_x(mu[0], sigma_x); //均值, 方差
	normal_distribution<double> n_y(mu[1], sigma_y); //均值, 方差

	vector<double> Offset;

	Offset.push_back(n_x(e));
	Offset.push_back(n_y(e));

	return Offset;
}

vector<double> FireStrike::getFiringDeviation(vector<double> sigma, vector<double> mu)
{
	static default_random_engine e(m_nSeed == 0 ? time(0) : m_nSeed); //引擎

	if (mu.size() < 2)
	{
		return mu;
	}

	if (sigma.size() < 2)
	{
		return sigma;
	}

	normal_distribution<double> n_x(mu[0], sigma[0]); //均值, 方差
	normal_distribution<double> n_y(mu[1], sigma[1]); //均值, 方差

	vector<double> Offset;

	Offset.push_back(n_x(e));
	Offset.push_back(n_y(e));

	return Offset;
}

void FireStrike::setSeed(int seed)
{
	m_nSeed = seed;
}

//void FireStrike::insertShootTable(string json)
//{
//	ShootTable table;
//
//
//
//	m_tables.push_back(table);
//}

void FireStrike::insertShootTable(ShootTable table)
{
	m_tables.push_back(table);
}

list<ShootTable> FireStrike::getShootTables()
{
	return m_tables;
}

ShootTable FireStrike::getShootTable(int id)
{
	ShootTable table;

	list<ShootTable>::iterator itor;
	for (itor = m_tables.begin(); itor != m_tables.end(); itor++)
	{
		table = *itor;

		if (table.m_nId == id)
		{
			break;
		}
	}

	return table;
}