import json
import requests
from bs4 import BeautifulSoup


def get_htmltext(url):
    try:
        r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        dict_datas = json.loads(r.text)
        return dict_datas['result']['data']
    except:
        return '产生异常'


def get_data_sk(data_lists):
    # soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    # body = soup.body
    # div = body.find('div', {'id': 'hdtable'})
    # print(div)
    print("{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t{:^10}\t".format('城市', '流域', '河名', '库名', '库水位', '蓄水量', '时间', '入库(米3/秒)'))
    for data_list in data_lists:
        chengshi = data_list['poiAddv']
        liuyv = data_list['poiBsnm']
        re_name = data_list['rvnm']
        shuiku_name = data_list['stnm']
        shuiku_hight = data_list['rz']
        shui_liang = data_list['wl']
        time = data_list['tm']
        ru_ku = data_list['inq']
        print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}\t{:^8}\t{:^8}\t{:^8}\t".format(chengshi, liuyv, re_name, shuiku_name, shuiku_hight, shui_liang, time, ru_ku))



data_lists = get_htmltext('http://xxfb.mwr.cn/hydroSearch/greatRsvr')
get_data_sk(data_lists)
