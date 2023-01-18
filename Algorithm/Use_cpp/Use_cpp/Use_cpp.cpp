// Random_test.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <vector>
#include <string>
#include <random>
#include <algorithm>
#include <cmath>
#include <numeric>
#include <fstream>

using namespace std;

void WriteFile(string data)
{
	ofstream outfile;
	outfile.open("D:\\Project_Files\\My_Projects\\Normal_Distribution\\ND_Random.json");

	// 向文件写入用户输入的数据
	outfile << data << endl;

	outfile.close();
}

string Normal_Distribution(string str, int num)
{
	static default_random_engine e(time(0)); //引擎
	normal_distribution<double> n_x(0, 0.68); //均值, 方差
	normal_distribution<double> n_y(0, 0.71); //均值, 方差

	int i_max = 1000;

	str += "\"";
	str += to_string(num);
	str += "\"";
	str += ":[";

	for (std::size_t i = 0; i <= i_max; i++) {
		double v_x = n_x(e); //取整-最近的整数
		double v_y = n_y(e); //取整-最近的整数
		str += "[";
		str += to_string(v_x);
		str += ",";
		str += to_string(v_y);
		if (i == i_max)
			str += "]],";
		else
			str += "],";
	}

	return str;
}

void Random()
{
	default_random_engine e;

	cout << "C++11 之前使用C语言的库， 最大周期为：32767" << endl;
	cout << "如今利用 C++14 测试，最大周期为：" << e.max() << endl;
	cout << "系统时间：" << time(0) << endl;
	cout << "系统时间的单位为秒，所以如果使用系统时间作为随机数种子，每秒最多可生成 " << e.max() << " 个独立的随机数" << endl;
	cout << "等下一秒再生成的随机数，因为随机数种子不同，所以是新的周期" << endl;

	return;
}

int main()
{
	string str = "{";
	for (int i = 1; i <= 6; i++)
	{
		str = Normal_Distribution(str, i);
	}
	str.pop_back();
	str += "}";

	WriteFile(str);

	//Random();

	return 0;
}
