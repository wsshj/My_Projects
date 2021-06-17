#pragma once

#include <iostream>

using namespace std;

class _declspec(dllexport) Parameter
{
public:
	float m_distance = 0;
	float m_spreadx = 1;
	float m_spready = 1;

	Parameter();
	Parameter(float distance, float spreadx, float spready);
	~Parameter();
};

