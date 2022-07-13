import requests
from bs4 import BeautifulSoup
import pymysql
import jieba

db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv"
)
cursor = db.cursor()
# cursor.execute("""drop table pu""")
cursor.execute("""CREATE TABLE pu口袋校园(name TEXT NOT NULL,url TEXT)""")


def huo_qv_xin_xi1(wangzhan):
    if __name__ == "__main__":
        p = 0
        wz = wangzhan
        zhuzhan = 'https://ahau.pocketuni.net/'
        req = requests.get(url=wz)
        fh = ''
        html = req.text
        bf = BeautifulSoup(html, features="html.parser")
        div = bf.find_all('div', class_='hd_c')
        a_bf = BeautifulSoup(str(div[0]), features="html.parser")
        for x in a_bf.select(".page a, .page a:visited"):
            if x.string == "下一页":
                p = 1
                fh = zhuzhan + x.get('href')
        if p == 1:
            return fh
        else:
            return 0


def huo_qv_xin_xi(wangzhan):
    if __name__ == "__main__":
        wz = wangzhan
        zhuzhan = 'https://ahau.pocketuni.net/'
        req = requests.get(url=wz)
        print(req)
        html = req.text
        bf = BeautifulSoup(html, features="html.parser")
        div = bf.find_all('div', class_='hd_c')
        print(div)
        a_bf = BeautifulSoup(str(div[0]), features="html.parser")
        a = a_bf.select('.hd_c_left_title a')
        for each in a:
            cha_ru(each)


def cha_ru(x):
    sql = "insert into pu口袋校园(name,url) VALUES ('%s','%s');" % (x.string, x.get('href'))
    print(x.string, x.get('href'))
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行1
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()


xiayiye = 'https://ahau.pocketuni.net/index.php?app=event&mod=School&act=board&&p=1'
while xiayiye != 0:
    huo_qv_xin_xi(xiayiye)
    xiayiye = huo_qv_xin_xi1(xiayiye)
db.close()