import requests
from bs4 import BeautifulSoup
# import execjs
import json
import pymysql
import re


db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv"
)
cursor = db.cursor()


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '产生异常'


def get_city(html):
    city = ''
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body = soup.body
    city1 = soup.find_all('div', class_='crumbs fl')
    city_bf = BeautifulSoup(str(city1), 'html.parser')
    a_city = city_bf.find_all('a')
    b_city = city_bf.find_all('span')
    # for a in a_city:
    #     print(a.string)
    # for b in b_city:
    #     print(b.string)
    num = len(a_city)
    num1 = len(b_city)
    city = city + b_city[num1 - 1].string
    city = a_city[num - 1].string + city
    print(city)
    return city

def get_data(html):
    final_list = []
    city = ''
    soup = BeautifulSoup(html, 'html.parser')  # 用BeautifulSoup库解析网页
    body = soup.body
    data = body.find('div', {'id': '7d'})
    ul = data.find('ul')
    lis = ul.find_all('li')

    for day in lis:
        temp_list = []

        date = day.find('h1').string  # 找到日期
        temp_list.append(date)

        info = day.find_all('p')  # 找到所有的p标签
        temp_list.append(info[0].string)

        if info[1].find('span') is None:  # 找到p标签中的第二个值'span'标签——最高温度
            temperature_highest = ' '  # 用一个判断是否有最高温度
        else:
            temperature_highest = info[1].find('span').string
            temperature_highest = temperature_highest.replace('℃', ' ')

        if info[1].find('i') is None:  # 找到p标签中的第二个值'i'标签——最高温度
            temperature_lowest = ' '  # 用一个判断是否有最低温度
        else:
            temperature_lowest = info[1].find('i').string
            temperature_lowest = temperature_lowest.replace('℃', ' ')

        temp_list.append(temperature_highest)  # 将最高气温添加到temp_list中
        temp_list.append(temperature_lowest)  # 将最低气温添加到temp_list中

        wind_scale = info[2].find('i').string  # 找到p标签的第三个值'i'标签——风级，添加到temp_list中
        temp_list.append(wind_scale)

        final_list.append(temp_list)  # 将temp_list列表添加到final_list列表中
    return final_list


# 用format()将结果打印输出
def print_data(final_list, num, city):
    print("{:^10}\t{:^8}\t{:^8}\t{:^8}\t{:^8}\t".format('日期', '天气', '最高温度', '最低温度', '风级'))
    for i in range(num):
        final = final_list[i]
        sql = "insert into HLkeshihua_weather(address,data,weather,max,min,wind) VALUES ('%s','%s','%s','%s','%s','%s');" % (city,final[0], final[1], final[2], final[3], final[4])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行1
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()


# 用main()主函数将模块连接
def main():
    city_url = 'https://j.i8tq.com/weather2020/search/city.js'
    city_all = getHTMLText(city_url)
    url = 'http://www.weather.com.cn/weather/'
    ym = 101010100
    wei = '.shtml'
    for i in range(330306):
        y = str(ym+i)
        if re.search(y, city_all):
            html = getHTMLText(url + str(y) + wei)
            city = get_city(html)
            final_list = get_data(html)
            print_data(final_list, 7, city)
        else:
            continue


main()
