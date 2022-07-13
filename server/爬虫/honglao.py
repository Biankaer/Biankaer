import json
import requests
from bs4 import BeautifulSoup


def get_htmltext(url):
    try:
        r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        dict_datas = json.loads(r.text)
        return dict_datas['result']
    except:
        return '产生异常'

def get_data_sk(data_lists):
    print("{:^10}\t{:^10}\t{:^10}\t{:^10}\t".format('地址', '站名', '时间', '汛情'))
    for data_list in data_lists:
        address = data_list['addv']
        name = data_list['stnm']
        time = data_list['tm']
        xunqing = data_list['zl']-data_list['wrz']
        print("{:^10}\t{:^10}\t{:^8}\t{:^10}\t".format(address, name, time, xunqing))


data_lists = get_htmltext('http://xxfb.mwr.cn/floodDroughtWarning/flood')
get_data_sk(data_lists)
