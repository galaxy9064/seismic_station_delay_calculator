"""
    处理数据，来自get_info获取的文件内容
"""
# 今天是一年的第几天
# from datetime import datetime
# day_of_year = datetime.now().timetuple().tm_yday

from get_info import get_delay, get_gapstat

# get_delay()

with open("gapstat_20220517_SN.F1002.txt","r") as gapstat_file:
    for line in gapstat_file:
        print(line)