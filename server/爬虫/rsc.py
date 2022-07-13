import json
import pymysql
import requests
from bs4 import BeautifulSoup
import re
from pymysql.converters import escape_string
# import sys  # 导入sys模块
# sys.setrecursionlimit(3000)

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


def cun(title, url, text):
    sql = """INSERT INTO ss_rsc
                        (title,url,text)
                        values
                        ("%s","%s","%s");"""
    try:
        cursor.execute(sql, (title, url, text))
        db.commit()
    except:
        db.rollback()


def get_title(html):
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    head = soup.head
    head_bf = BeautifulSoup(str(head), 'html.parser')
    title = head_bf.find('title')
    all_titles.append(title)
    if title !=None:
        return title.string


def get_data(html, url):
    if len(url) > 900:
        return 'error'
    surl = []
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    for a in soup.find_all('a', href=True):
        link = a['href']
        if link not in all_urls and link != "javascript:;" and link != "#":
            if re.search('rsc.ahau', link) and re.search('http', link):
                surl.append(link)
            else:
                if re.search(link, url):
                    continue
                else:
                    lurl = jq(url, link)
                    surl.append(lurl)
    for s in surl:
        if s not in all_urls:
            print(s)
            html = get_html(s)
            if html == 'error':
                continue
            else:
                all_urls.append(s)
                title = get_title(html)
                all_titles.append(title)
                # all_html.append(html)
                get_data(html, s)
                # print(title)
                # print(s)
                cun(title, s, html)


head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29 "
}
if __name__ == "__main__":
    ahau_url = "http://rsc.ahau.edu.cn/"
    all_titles = ["安徽省“知名专家”-安徽农业大学-人事处"]
    all_urls = []
    all_html = []
    all_urls.append(ahau_url)
    ahau_html = get_html(ahau_url)
    all_html.append(ahau_html)
    cun(all_titles, ahau_url, ahau_html)
    get_data(ahau_html, ahau_url)
    for i in range(len(all_urls)):
        print(all_urls[i])
    #     s_html = get_html(all_urls[i])
    #     cun(all_titles[i], all_urls[i], s_html)
    # print(all_titles)
    # print(all_urls)
