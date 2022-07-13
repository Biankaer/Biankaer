import datetime
import json
import sys
import pymysql
import requests
from bs4 import BeautifulSoup
import re
import threading
import scrapy
from pymysql.converters import escape_string

# import sys  # 导入sys模块
# sys.setrecursionlimit(100000)
sys.setrecursionlimit(3000)

db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv",
    autocommit=True
)
cursor = db.cursor()


def get_html(url):
    session = requests.Session()
    try:
        r = session.post(url, timeout=5, headers=head)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return 'error'


def get_Data(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    body = soup.body
    all_Data = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", html)
    if len(all_Data) > 0:
        return all_Data[0]
    else:
        return None
        # all_Data1 = re.findall(r"(\d{4}.\d{1,2}.\d{1,2})", str(body))
        # if all_Data1[0] is not None:
        #     return all_Data1[0]
        # else:
        #     return datetime.datetime.now()


def jq(url, link):
    wz = url.rfind('/')
    url = url[0:wz]
    for i in range(10):
        if link.find('/') == 2:
            wz = url.rfind('/')
            url = url[0:wz]
            link = link[3:]
        else:
            break
    return url + '/' + link


def Dw(url):
    s = url.find('cn')
    main_url = url[7:s + 2]
    if main_url == 'zsb.ahau.edu.cn':
        return "安徽农业大学-招生信息网本科"
    else:
        if main_url == 'app.ahau.edu.cn':
            return "安徽农业大学录取查询验证及录取通知书EMS跟踪查询"
    source = get_title(main_url)
    if source == None:
        return "安徽农业大学"
    return source


def truncate():
    sql = "truncate table ss_ahau;"
    cursor.execute(sql)
    db.commit()


def cun(title, url, text, date, source):
    sql = """INSERT INTO ss_ahau(`title`,`url`,`text`,`ss_date`,`source`) values (%s,%s,%s,%s,%s)"""
    # try:
    cursor.execute(sql, (title, url, text, date, source))
    db.commit()
    # except:
    #     db.rollback()


def get_Text(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup_h = soup.find_all('h1')
    h = ''
    for i in soup_h:
        if i.string is None:
            continue
        h = h + i.string
    soup_p = soup.find_all('p')
    for i in soup_p:
        if i.string is None:
            continue
        h = h + i.string
    soup_span = soup.find_all('span')
    for i in soup_span:
        if i.string is None:
            continue
        h = h + i.string
    return h


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    head = soup.head
    head_bf = BeautifulSoup(str(head), 'html.parser')
    title = head_bf.find('title')
    all_titles.append(title)
    if title != None:
        return title.string


def get_data(html, url):
    # if len(url) > 900:
    #     return 'error'
    surl = []
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    for a in soup.find_all('a', href=True):
        link = a['href']
        if link not in all_urls and link != "javascript:;" and link != "#":
            if re.search('ahau.edu', link) and re.search('http', link):
                surl.append(link)
            else:
                try:
                    if re.search(link, url):
                        continue
                    else:
                        lurl = jq(url, link)
                        surl.append(lurl)
                except:
                    print(link, url)
    for s in surl:
        if s not in all_urls:
            html = get_html(s)
            if html == 'error':
                continue
            else:
                all_urls.append(s)
                title = get_title(html)
                all_titles.append(title)
                text = get_Text(html)
                # all_html.append(html)
                str_data = get_Data(html)
                if str_data is not None:
                    data = datetime.datetime.strptime(str_data, '%Y-%m-%d')
                    data.strftime('%Y-%m-%d')
                else:
                    data = datetime.datetime(2012, 1, 1)
                get_data(html, s)
                source = Dw(s)
                # print(title)
                # print(s)
                if title is not None:
                    cun(title, s, text, data, source)


head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29 "
}
if __name__ == "__main__":
    sql1 = "SELECT url FROM ss_ahau;"
    cursor.execute(sql1)
    results = cursor.fetchall()
    # truncate()
    all_urls = []
    ahau_url = "https://www.ahau.edu.cn/"
    # ahau_url = "http://i.ahau.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__&ticket=ST-801380-qRrP4PGbggPV29B7xZPc-ee4c9b15b24a"
    all_titles = ["安徽农业大学"]
    for s in results:
        all_urls.append(s[0])
        # print(s[0])
    # all_urls = []
    # # all_html = []
    all_urls.append(ahau_url)
    ahau_html = get_html(ahau_url)
    ahau_data = get_Data(ahau_html)
    # all_html.append(ahau_html)
    ahau_text = get_Text(ahau_html)
    # cun(all_titles[0], ahau_url, ahau_text, ahau_data, all_titles[0])
    # t1 = threading.Thread(target=get_data, args=(ahau_html, ahau_url))
    # t1.start()
    # t2 = threading.Thread(target=get_data, args=(ahau_html, ahau_url))
    # t2.start()
    # t3 = threading.Thread(target=get_data, args=(ahau_html, ahau_url))
    # t3.start()
    get_data(ahau_html, ahau_url)
    # for i in range(len(all_urls)):
    #     print(all_urls[i])
    # print(len(all_urls))
    #     s_html = get_html(all_urls[i])
    #     cun(all_titles[i], all_urls[i], s_html)
    # print(all_titles)
    # print(all_urls)
