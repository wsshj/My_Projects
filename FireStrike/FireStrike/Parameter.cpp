#include "pch.h"
#include "Parameter.h"

Parameter::Parameter()
{
}

Parameter::Parameter(float distance, float spreadx, float spready)
{
	m_distance = distance;
	m_spreadx = spreadx;
	m_spready = spready;
}

Parameter::~Parameter()
{
}
