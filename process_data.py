"""
    处理数据，来自get_info获取的文件内容
"""
# 今天是一年的第几天
# from datetime import datetime
# day_of_year = datetime.now().timetuple().tm_yday
import time

import get_info

# get_info.get_station_channels()

station_list = []
tic1 = time.time()
with open("station_channels.txt", "r") as station_list_file:
    initial_line = True
    for line in station_list_file:  # 获取所有台站名
        if initial_line:  # 跳过第一行"OK 42279 JOPENS/AWS 1.1R, RESTful Interface, Channel List:"
            initial_line = False
        else:
            split_line = line.split(".")
            station_list.append(split_line[1])
    print(station_list)
    station_list = list(set(station_list)) # 排除重复台站名
    station_list.sort()  # sort()直接对list重新排序，返回none type
    print(station_list)

tic2 = time.time()
print("耗时%f秒" % (tic2 - tic1))

# get_info.get_delay()

# with open("gapstat_20220517_SN.F1002.txt","r") as gapstat_file:
#     for line in gapstat_file:
#         print(line)

# 生成一个（台站数，24）的二维列表，默认填充
