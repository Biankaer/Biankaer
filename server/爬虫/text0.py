import json
import requests
from bs4 import BeautifulSoup
import re


def get_html(url):
    try:
        html = requests.get(url, timeout=30)  # 用requests抓取网页信息
        html.raise_for_status()  # 可以让程序产生异常时停止程序
        html.encoding = 'utf-8'
        return html.text
    except:
        return 'error'


def get_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    head = soup.head
    title = head.find('title').string
    return title


html = get_html("http://i.ahau.edu.cn/_web/fusionportal/index.jsp?_p=YXM9MSZwPTEmbT1OJg__")
title = get_title(html)
print(title)
