import pymysql
import re
import json

db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv"
)
cursor = db.cursor()
shuchu = []
sql = "SELECT * FROM pu口袋校园;"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        if re.search('大赛', row[0]):
            shuchu += row
except:
    print("Error: unable to fetch data")
num = len(shuchu)
name = []
url = []
for i in range(num):
    if i % 2 == 0:
        name.append(shuchu[i])
    else:
        url.append(shuchu[i])
for i in name:
    print(i)
name_zd = dict(enumerate(name))
url_zd = dict(enumerate(url))
print(name_zd)
print(url_zd)
