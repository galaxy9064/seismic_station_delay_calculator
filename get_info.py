"""
    通过http协议获取台站延时数据
"""

import requests

session_jopens = requests.sessions.session()


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
# # 获取台站通道信息
# url_station_channels = "http://21.124.7.3:8080/jopens-ws/app/aws/menu"
# r = session_jopens.get(url_station_channels)
# with open("station_channels.txt", "wb") as file:
#     file.write(r.content)
#
# # 获取台站断记时长（一小时一行） url_gapstat = "http://21.124.7.3:8080/jopens-ws/app/aws/gidx;jday=137;year=2022;chan=SN.F1002.40
# .EIE;type=GAPSTAT;nday=1" r = session_jopens.get(url_gapstat) with open("gapstat_20220517_SN.F1002.txt",
# "wb") as file: file.write(r.content)

def get_gapstat():
    # 获取台站断记时长（一小时一行,一天24行）
    url_gapstat = "http://21.124.7.3:8080/jopens-ws/app/aws/gidx;jday=137;year=2022;chan=SN.F1002.40.EIE;type=GAPSTAT;nday=1"
    r = session_jopens.get(url_gapstat)
    with open("gapstat_20220517_SN.F1002.txt","wb") as file:
        file.write(r.content)

def get_delay():  # 获取台站延时信息（一分钟一行，一天1440000行）
    uri_delay="uri=/usr/local/wildfly21/standalone/log/delay.log.2022-05-01"
    url_delay = "http://21.124.7.3:8080/JOPENSWeb/mon/logDownload?"+uri_delay
    r = session_jopens.get(url_delay)
    with open("delay_20220501.log", "wb") as file:
        file.write(r.content)
