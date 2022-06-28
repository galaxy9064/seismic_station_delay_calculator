"""
    处理数据，来自get_info获取的文件内容
    v0.1.220601 从channel文件中获取台站列表
    v0.3.220628 读取延迟文件并存入字典（速度较慢）
"""
# 今天是一年的第几天
# from datetime import datetime
# day_of_year = datetime.now().timetuple().tm_yday
import re
import time
import datetime
import get_info

#  获取台站信道信息函数
# get_info.get_station_channels()

list_sta_id = []
tic1 = time.time()
# 从文件中提取站名列表
with open("station_channels.txt", "r") as station_list_file:
    initial_line = True
    for line in station_list_file:  # 获取所有台站名
        if initial_line:  # 跳过第一行"OK 42279 JOPENS/AWS 1.1R, RESTful Interface, Channel List:"
            initial_line = False
        else:
            split_line = line.split(".", maxsplit=2)
            list_sta_id.append(split_line[0] + "/" + split_line[1])  # station id for example: SN.A0001
    print(list_sta_id)
    list_sta_id = list(set(list_sta_id))  # 排除重复台站名
    list_sta_id.sort()  # sort()直接对list重新排序，返回none type
    print("台站列表：" + str(list_sta_id))

tic2 = time.time()
print("获取台站列表，耗时%f秒" % (tic2 - tic1))

# 获取延时信息
#   1.输入起止日期
#   2.下载指定日期的延时文件
#   3.计算平均延时

# 1.输入起止日期
while (True):
    str_start_date = input("请输入起始日期(格式为yyyymmdd)：")

    try:  # 检查日期格式是否正确，并转换
        # <strptime> Parse a string to a time tuple
        datetime_start_date = datetime.datetime.strptime(str_start_date, "%Y%m%d")
        print(type(datetime_start_date))
        print(datetime_start_date)

        break
    except:
        print("日期输入有误！请重新输入")

# filename_str = str_date_from_datetime+".delay.log"
# print(filename_str)

# 2. 输入日期范围，下载指定日期的延时文件
int_days_last = 1
while (True):
    try:  # 检查输入天数是否为正整数
        int_days_last = int(input("请输入持续天数："))
        if int_days_last > 0:
            break
        else:
            print("不能为零或负！请重新输入天数：")
    except:  # ValueError
        print("数值输入错误！请重新输入天数：")

list_date = []
list_delay_filename = []
for days_add in range(0, int_days_last, 1):
    # 逐个生成指定范围内的日期:起始日期+n天
    datetime_temp_date = datetime_start_date + datetime.timedelta(days=days_add)
    list_date.append(datetime_temp_date)
    # datetime转日期字符串
    str_date_from_datetime = datetime_temp_date.strftime("%Y-%m-%d")
    list_delay_filename.append(str_date_from_datetime)
    # 根据日期字符串下载延迟文件
    get_info.get_delay(str_date_from_datetime)
# print(list_date)
# print(list_delay_filename)


# 创建字典,按照格式{string:list,string:list}保存延时信息
# 如 {'SN/A0001':[0.73,0.75],'SN/A002':[0.98,0.93]}
dict_sta_delay = {}
for sta_id in list_sta_id:
    dict_sta_delay[sta_id] = []

# 从延迟文件中提取各台站延迟
# 第一层：逐个读取各延迟文件 第二层 逐行匹配台站名
for str_delay_date in list_delay_filename:  # 第一层
    with open("delay.log." + str_delay_date) as delay_filestream:
        # 方法1：逐行读取文件信息，进行台站ID匹配
        tic1 = time.time()
        for delay_line in delay_filestream:  # 第二层
            _ = re.split(r"(?:,)|(?:\s+)", delay_line, maxsplit=7)
            # Regexp: (?:...)表示非捕获分组，\s+表示连续多个空格只匹配一次
            split_delay_line = list(filter(None, _))
            # print(split_delay_line)
            if len(split_delay_line) > 0: #如果不加判断，空行split_delay_line[0]会报错
                for sta_id in list_sta_id:
                    if sta_id == split_delay_line[0]:
                        # type(dict_sta_delay[sta_id]) -> list
                        dict_sta_delay[sta_id].append(split_delay_line[1])
                        # print(dict_sta_delay)
                        break
        # print(dict_sta_delay) # 应有1000个键值对，每个值长度为1440秒
        tic2 = time.time()
        print("方法1：逐行读取文件信息，检索台站ID匹配，耗时%f秒" % (tic2 - tic1))

        # #方法2：根据规律预测行号，直接去指定行读取
        # indexed_delay_filestream=enumerate(delay_filestream)
        # print(list(indexed_delay_filestream))
    # for sta_id in list_sta_id:
