import re
import sys
import threading
from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
import pymysql
import jieba
import json

lock = threading.Lock()
sys.setrecursionlimit(2000)
db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv"
)
cursor = db.cursor()


# Create your views here.


def index(request):
    return render(request, 'index.html')


def sousuo(all_name, sword, name, url, i, j, results):
    cursor = db.cursor()
    for row in range(i, j):
        all_name.append(results[row][0])
        if re.search(sword, results[row][0]):
            name.append(results[row][0][1:-1])
            url.append(results[row][1][1:-1])
            # shuchu += row
            # print(shuchu)
    for n in range(i, j):
        lock.acquire()
        sql2 = "SELECT title,url,text FROM ss_ahau where id='%d';" % (n)
        cursor.execute(sql2)
        # 获取所有记录列表
        results2 = cursor.fetchall()
        lock.release()
        for r in results2:
            if re.search(sword, r[2]) and r[1][1:-1] not in url:
                name.append(r[0][1:-1])
                url.append(r[1][1:-1])


def Dw(word, text):
    s = int(text.find(word))
    if s >= 5:
        if len(text[s:]) > 40:
            return s-5, s + 40
        else:
            return s-5, -1
    else:
        if len(text[s:]) > 40:
            return 0, s + 40
        else:
            return 0, -1
    # s = text.find(word)
    # if len(s)<=1:
    #     if len(text[s[0]:]) > 15:
    #         return s[0], s[0] + 15
    #     else:
    #         return s[0], text[-1]
    # else:
    #     if s[-1] - s[0] < 15:
    #         return s[0], s[-1]
    #     else:
    #         if len(text[s[0]:]) > 15:
    #             return s[0], s[0] + 15
    #         else:
    #             return s[0], text[-1]


sql1 = "SELECT title,url,text,ss_date,source FROM ss_ahau order by ss_date DESC;"
cursor.execute(sql1)
results = cursor.fetchall()


def ss(word, all_Data):
    for row in results:
        Data = {}
        # all_name.append(row[0])
        if re.search(word, row[0]) or re.search(word, row[2]):
            Data['title'] = row[0]
            Data['url'] = row[1]
            i, j = Dw(word, row[2])
            Data['text'] = row[2]
            Data['date'] = row[3]
            Data['source'] = row[4]
            all_Data.append(Data)



def search(request):
    sword = request.GET.get('s_word')
    print(sword)
    name = []
    all_name = []
    url = []
    all_Data = []
    sql = 'select id from ss_ahau;'
    db.ping(reconnect=True)
    cursor.execute(sql)
    db.commit()
    if not sword:
        return render(request, 'error.html')
    shuru_fen = jieba.cut_for_search(sword)
    print(list(shuru_fen))
    shuchu = []
    sql1 = """SELECT `title`,`url` FROM ss_ahau;"""
    cursor.execute(sql1)
    results = cursor.fetchall()
    len1 = len(results)
    sousuo(all_name, sword, name, url, 0, len1 // 3, results)
    # t1 = threading.Thread(target=sousuo, args=(all_name, sword, name, url, len1 // 3, len1 * 2 // 3, results))
    # t2 = threading.Thread(target=sousuo, args=(all_name, sword, name, url, len1 // 3, len1, results))
    # t1.start()
    # t2.start()
    t = threading.Thread(target=ss, args=(sword, all_Data))
    t.start()
    shuru_fen = jieba.cut_for_search(sword)
    num = len(all_Data)
    return render(request, 'results.html',
                  {'name': name, 'url': url, 'num': num, 'data': all_Data, 'json_Data': json.dumps(all_Data, ensure_ascii=False, default=str)})
