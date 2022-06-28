"""
    通过http协议获取台站数据
    v0.1 使用requests库，sessions保持连接，get发送get请求
    v0.2 get_delay(date_input)函数,加入输入参数date_input:str
    v0.3.220628 加入连接异常的处理机制，可以手动导入延迟数据

"""

import requests
from requests.exceptions import ConnectTimeout  # 报错不影响运行 Cannot find reference 'ConnectTimeout' in '__init__.pyi'

session_jopens = requests.sessions.Session()


# # 使用POST登录jopens-sss
# url_login_sss = 'http://21.124.7.3:8080/jopens-sss/sss/login2'# 登录
# d = {'user': 'root', 'pass': 'JOPENS@yj_328'}
# r = session_jopens.post(url_login_sss, data=d)
# with open("login_response.html", 'wb') as file:
#     file.write(r.content)
#
# # url_logout_sss = 'http://21.124.7.3:8080/jopens-sss/sss/logout'# 注销
# # r=session_jopens.get(url_logout_sss)
# # with open("logout_response.html","wb")as file:
# #     file.write(r.content)
#
# # 使用GET获取台站名等信息(需要先登录)
# url_sss_stations = 'http://21.124.7.3:8080/jopens-sss/config/sssStations.json'
# r = session_jopens.get(url_sss_stations)
# with open("ybz_sss_stations.html", "wb") as file:
#     file.write(r.content)
#


def get_station_channels():
    # 获取台站通道信息
    url_station_channels = "http://21.124.7.3:8080/jopens-ws/app/aws/menu"
    r = session_jopens.get(url_station_channels)
    print(r.headers)
    with open("station_channels.txt", "wb") as file:
        file.write(r.content)


def get_gapstat():
    # 获取台站断记时长（一小时一行,一天24行）
    url_gapstat = "http://21.124.7.3:8080/jopens-ws/app/aws/gidx;jday=137;year=2022;chan=SN.F1002.40.EIE;type=GAPSTAT;nday=1"
    r = session_jopens.get(url_gapstat)
    with open("gapstat_20220517_SN.F1002.txt", "wb") as file:
        file.write(r.content)


def get_delay(date_input):  # 获取台站延时信息（一分钟一行，一天1440000行）
    delay_filename = "delay.log." + date_input
    uri_delay = "uri=/usr/local/wildfly21/standalone/log/" + delay_filename
    url_delay = "http://21.124.7.3:8080/JOPENSWeb/mon/logDownload?" + uri_delay
    # url_delay = "http://21.4.7.2:8080/JOPENSWeb/mon/logDownload?" + uri_delay
    try:
        # session.get获取延时数据文件，自定义超时阈值
        r = session_jopens.get(url_delay, timeout=1)
        print("status_code:" + str(r.status_code))
        with open(delay_filename, "wb") as file:
            file.write(r.content)
    except Exception as e:
        print("%s获取失败" % delay_filename)
        print("错误信息：" + str(e))
