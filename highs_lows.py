# -*- coding: utf-8 -*-
# @Author: Clarence
# @Date:   2018-03-24 16:06:27
# @Last Modified by:   Clarence
# @Last Modified time: 2018-03-24 19:12:38
"""
在文本文件中存储数据，最简单的方式是将数据作为一系列以
逗号分隔的值(CSV)写入文件，这样的文件称为CSV文件
sitka_weather_07-2014.csv文件中是阿拉斯加锡特卡2014年的天气数据
，其中包含当天的最高气温和最低气温
我们可以使用Python标准库中的csv模块来读取文件
大家不要怕，我知道有一些翻译好了的中文手册，但是我还是希望自己可以看懂英文文档，我不希望出现了新的技术
还要等国内大神翻译一下才能看。我和大家一起看文档，翻译。
enumerate()内置函数的使用方法
enumerate(iterable, start = 0)
	Return an enumerate object. iterable must be a sequence, an iterator, or some
other object which supports iteration. The __next__() method of the iterator returned
by enumerate() returns a tuple containing a count(from start which defaults to 0)
and the values obtained from iterating over iterable.
这个意思就是eumerate()方法返回一个美剧对象，iterabel参数必须是一个序列、迭代器、或者其他支持迭代的对象。
由enumerate()返回的迭代器的__next__()方法，会返回一个包含计数(默认从0开始)的元组，包含的值来自迭代器的迭代
>>> seasons = ['Spring', 'Summer', 'Fall', 'Winter']
>>> list(enumerate(seasons))
[(0, 'Spring'), (1, 'Summer'), (2, 'Fall'), (3, 'Winter')]
>>> list(enumerate(seasons, start=1))
[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')]
我们显示出来锡特卡的最高气温和最低气温

打开死亡谷的温度数据集death_valley_2014.csv
可以发现文件中有某一行的最高气温是空的，这样可就产生了ValueError异常
因此我们要添加一些捕获异常代码try-except-else
学过java的我们都知道用try-catch-finally
"""

import csv 
from matplotlib import pyplot as plt
from datetime import datetime

#filename = 'sitka_weather_2014.csv'
filename = 'death_valley_2014.csv'
with open(filename) as f:
	# f为文件对象，调用csv的reader方法传递参数，得到与该文件相关联的阅读器对象
	reader = csv.reader(f)
	# 模块csv包含next()函数，传入参数reader,将返回文件中的下一行
	header_row = next(reader)
	'''
	#得到的数据就是用Excel打开文件之后的第一行数据4列表
	print(header_row)
	for index, column_header in enumerate(header_row):
		print(index, column_header, sep = ':')
	0:AKDT
	1:Max TemperatureF
	2:Mean TemperatureF
	3:Min TemperatureF
	4:Max Dew PointF
	5:MeanDew PointF
	6:Min DewpointF
	7:Max Humidity
	8: Mean Humidity
	9: Min Humidity
	10: Max Sea Level PressureIn
	11: Mean Sea Level PressureIn
	12: Min Sea Level PressureIn
	13: Max VisibilityMiles
	14: Mean VisibilityMiles
	15: Min VisibilityMiles
	16: Max Wind SpeedMPH
	17: Mean Wind SpeedMPH
	18: Max Gust SpeedMPH
	19:PrecipitationIn
	20: CloudCover
	21: Events
	22: WindDirDegrees
	[Finished in 0.6s]
	可以看到最高气温和最低气温分别存储在第0列和第1列
	为了研究这些数据，我们将提取文件中每行数据，并提取索引值为1和2的值

	图表的横坐标应该是对应的日期，因此我们需要导入datetime模块中的datetime类
	classmethod datetime.strptime(date_string, format)
		Return a datetime corresponding to date_string, parsed according to format.
	也就是说strptime方法有两个参数,一个是日期字符串，另一个是日期格式，根据日期格式解析字符串，
	返回一个日期对象
	'''

	#提取最高气温和最低气温日期
	dates, highs, lows= [], [], []
	# 大家注意，此时文件指针在第二行
	for row in reader:
		try:
			# 日期格式为年月日
			current_date = datetime.strptime(row[0], "%Y-%m-%d")
			# int()便于matplotlib读取
			high = int(row[1])
			low = int(row[2])
		except ValueError:
			print(current_date, 'missing data')
		else:
			dates.append(current_date)
			highs.append(high)
			lows.append(low)

	#根据数据绘制图形
	#设置屏幕分辨率dpi=128像素/英寸 屏幕尺寸长宽5/3英寸
	fig = plt.figure(dpi = 128, figsize = (5, 4))
	#alpha参数指定颜色的透明度，0表示完全透明，默认为1表示完全不透明
	plt.plot(dates, highs, c = 'red', alpha = 0.5)
	plt.plot(dates, lows, c = 'blue', alpha = 0.5)
	#fill_between方法接受一个x值系列和两个y值系列，并填充两个y值系列之间的空间 facecolor为填充颜色
	plt.fill_between(dates, highs, lows, facecolor = 'blue', alpha = 0.1)

	# 设置图形的格式
	#plt.title("Daily high temperatures - 2014", fontsize = 12)
	plt.title("Daily high and low temperatures - 2014\nDeath Valley, CA")
	plt.xlabel('', fontsize = 10)
	# 自动调整横坐标日期
	fig.autofmt_xdate()
	# 华氏温度F = 95C + 32
	plt.ylabel("Temperature (F)", fontsize = 10)
	plt.tick_params(axis = 'both', which = 'major', labelsize = 8)

	plt.show()



