import json
import pymysql
import requests
from bs4 import BeautifulSoup
import re

db = pymysql.connect(
    host="localhost",  # 数据库主机地址
    user="root",  # 数据库用户名
    passwd="root",  # 数据库密码
    database="shujv"
)
cursor = db.cursor()



def get_html(url):
    s = session = requests.Session()
    try:
        r = session.post(url, timeout=5, headers=head, data=data)  # 用requests抓取网页信息
        # r = requests.get(url, timeout=30)  # 用requests抓取网页信息
        r.raise_for_status()  # 可以让程序产生异常时停止程序
        r.encoding = r.apparent_encoding
        # print(r.text)
        return r.text
    except:
        return 'error'


def get_data(html):
    surl = []
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    head = soup.find('head')
    # title = head.title.string
    # title = str(head).find('title')
    for a in soup.find_all('a', href=True):
        link = a['href']
        if link not in all_urls and link != "javascript:;":
            if re.search('http', link) and re.search('ahau', link):
                surl.append(link)
            # else:
            #     surl.append(html+'/'+link)
            #     print(html+'/'+link)
            # if re.search('http', link):
            #     all_urls.append(link)
            # else:
            #     all_urls.append(html+'/'+link)
    for s in surl:
        if s not in all_urls:
            html = get_html(s)
            if html == 'error':
                continue
            else:
                get_title(html)
                # print(title)
                # print(s)
                all_urls.append(s)
                # get_data(html)
    # soup = BeautifulSoup(html, 'html.parser')
    # body = soup.body
    # # print(str(body))
    # surl = re.findall(r'http[^/]{1,2}//([^(/| ")]+)', str(body))
    # return surl
    # for s in surl:
    #     if s not in all_urls:
    #         all_urls.append(s)


def get_title(html):
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()
    head = soup.head
    # title = head.title.string
    head_bf = BeautifulSoup(str(head), 'html.parser')
    title = soup.find_all('title')
    for tit in title:
        all_titles.append(tit.string)


# def get_all1(urls, titles):
#     i = 0
#     for url in urls:
#         if re.search('ahau', url) and re.search('yjsc.ahau.edu.cn', url) is None and re.search('aistead.ahau.edu.cn', url) is None and re.search('https://www.ahau.edu.cn/', url) is None and re.search('vpn', url) is None and re.search('mail', url) is None and re.search('ahauetc', url) is None and re.search('app.ahau.edu.cn', url) is None and re.search('rsxt.ahau.edu.cn', url) is None and re.search('newjwxt.ahau.edu.cn', url) is None and re.search('cms.ahau.edu.cn:8888', url) is None and re.search('marx.w1.ahau.edu.cn', url) is None and re.search('zcjxy.w1.ahau.edu.cn', url) is None and re.search('zhxy.w1.ahau.edu.cn', url) is None and re.search('jgxy.w1.ahau.edu.cn', url) is None and re.search('nyswjs.ahau-edu.cn', url) is None and re.search('ahau.ihwrm.com', url) is None and re.search('ids2.ahau.edu.cn', url) is None and re.search('pcsb.ahau.edu.cn', url) is None and re.search('bdcms.ahau.edu.cn', url) is None and re.search('xyhui.w1.ahau.edu.cn', url) is None:
#             html = get_html("https://" + url)
#             if html == 'error':
#                 continue
#             else:
#                 tit = get_title(html, titles)
#                 print(tit)
#                 if tit not in titles:
#                     print(url)
#                     i = i + 1
#                     all_titles.append(tit)
#                     ls_urls = get_url(html)
#                     for u in ls_urls:
#                         if u not in all_urls:
#                             all_urls.append(u)
#                     # get_all(ls_urls, titles)
#                 else:
#                     continue
#     print(i)
#     # return urls, titles
#
#
# def get_all(urls, titles):
#     # i = 0
#     for url in urls:
#         if re.search('ahau', url) and re.search('yjsc.ahau.edu.cn', url) is None and re.search('aistead.ahau.edu.cn', url) is None and re.search('https://www.ahau.edu.cn/', url) is None and re.search('vpn', url) is None and re.search('mail', url) is None and re.search('ahauetc', url) is None and re.search('app.ahau.edu.cn', url) is None and re.search('rsxt.ahau.edu.cn', url) is None and re.search('newjwxt.ahau.edu.cn', url) is None and re.search('cms.ahau.edu.cn:8888', url) is None and re.search('marx.w1.ahau.edu.cn', url) is None and re.search('zcjxy.w1.ahau.edu.cn', url) is None and re.search('zhxy.w1.ahau.edu.cn', url) is None and re.search('jgxy.w1.ahau.edu.cn', url) is None and re.search('nyswjs.ahau-edu.cn', url) is None and re.search('ahau.ihwrm.com', url) is None and re.search('ids2.ahau.edu.cn', url) is None and re.search('pcsb.ahau.edu.cn', url) is None and re.search('bdcms.ahau.edu.cn', url) is None and re.search('xyhui.w1.ahau.edu.cn', url) is None:
#             html = get_html("https://" + url)
#             tit = get_title(html, titles)
#             print(tit)
#             if tit not in titles:
#                 print(url)
#                 # i = i + 1
#                 all_titles.append(tit)
#                 ls_urls = get_url(html)
#                 for u in ls_urls:
#                     if u not in all_urls:
#                         all_urls.append(u)
#                 get_all(ls_urls, titles)
#             else:
#                 continue
#     print(i)
#     # return urls, titles


head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29 "
}
data = {
    'username': '20115171',
    'password': '11a884812d012dbb2dd1c49de554917ed68fb0b3f8593d3eca4226bb361b9dc36431dc5c0fd76fd1e87a0c9c6c412650544cf5e8143f41ac266d60a118e0dd5b5717bf3e9d9a3da5c9fdb155158f4d0959010a588ea9d4f4f04ab8fe210da1a993437642fc0c2f6b6f92ff9068c9afc631f0f169d72d1623adc8c589207ebb8b',
    'execution': "220e9e18-8c3d-459a-b99a-e89fdb456737_ZXlKaGJHY2lPaUpJVXpVeE1pSjkuTm1GbFRETklMMDFuYldWNGJrdEpka1ZLY0RWSlNWSkRSMEpqUW1Sd09FVTJPV2c0VWxCTlJVcEplbkI0SzBOemRsQlNlRFJqWXpKSFpHTlVTbmhPTmtSblZsWXhlbFZ4WmxCemFHWk9ZMFJ3SzJvM1l6aG9WMDFIYlZKMGFFcGFPVXRUTjAxdmRYZFpjRzlCYlVWd1oxazRWR0pIZW1aWEszUnhNRXRyWTNoa2VGWlNSak5HWTBSWGRFbEZlRUp2Y25SdFVVdFRjRTltZFRCVVJYRkVOMVZqV25JNWFXSnBSSE5aTUdwR2RUa3lNMWMxZGt0UVNFY3lNRlZUYlVKWWRGVjNORVppTm1FeVMyaGpSWGg1T0d3dlVqVjZWV055YkZJeVYzcHNOa2xvVkdZdlNrOUxNMk5EYzA5WWNreEtibEJQWWxZcmVVYzNSMlpyU1dOck0yWmhSaXR1WkZSM1NFY3hiVzlZUWpGa1FuZFVlRFpYZEVvcllVZHZTbFJVWTBjelJVOUhjWEpOV2tSaU1TOTJRbWRCUW5WcmR6RkhMMnA2ZDNSNFZqRXhMMjVvWTNaQ1l5ODViV2R2TDA1cFJuQm1jSGhpY25SclRXaGhja05rVURoSlMzZzJiMnBKUzJaelRIZHNVM0J1WjNsWFpVeFlWREExV1dkRlprTkhXVVJsVjBoS1JHb3pTRzFGTTJOcU56bGpkR294VFZkdVJrZFlVMVF2Um5wdFNrdHZaSEUxTm1SaWFYUjBhRTlaUmxRME5XWmtUV05LV210RlozVk9Va1UwWjB0VE5VNW5iSGhVY2treFdsSjRXbEJDWlhCS2RqbENLMUZDTWl0blUxbzVWblZsYlV4NFptSmtSRE5pUWpoaU5WWktPRTl0YWpOU01rSlZaRWhRTkd0M1ZHY3lSVzVZU0RVemQyNXpkalY2TmpkUU9VZzNMMjlhUVU0NWN6bFFXV1p1VFdkWmJHdFZjWEJSZEhwTlFtaHBWbVp3UTA1T1oxZFZibmRDZDNsNFZ6WmpSbU5hZGpRMWFFeElWV2xRTWtGVFdXUklOVWxuT0hGRU5rOUxNa2RGWWxSMlRXSkpNV3A1TTNkdlkzZElVa3cxVGxoSWFGbGplbGRWVXpaMlFuTlNhbW93VW1wS1FuYzBPRVUwYVhkb1dqaFZjVzVYT0c5T1RTOHZOV1I1ZDB0QlVITnhZVkV2YzFOSVozRnBNR1l6ZDI5MmVXNUxjbkJGYUUxdk4zaHZTVGRuVUhVck9XZEVURE5wVldoaGJETkdjbGhCWlhKVFp5dDZUR2REVVUxSFZqTmpka3RhUjBoWGIzbFNValZMVVUxQk1EZHlkSEZqS3paSlNHTXdibFZaSzFoV1FWWXljMjlpVldoeFZtNUlaRzFUTjNaM2RWWlJUREo1TTJkS04wVkdlVlp6UTNSRGRURXZUMnAzVmxWTUwzRXZNVmd6VlVFek0yY3hSVTFoTkVKV2VYUlhaRVJTZDBzeldWVlJVbmRYU2pKdFkyMUNSRFIzVDBVeFpXeFlXaXQ0VWlzMlRWWnZiMkppY0VRMVdISXhja3BTTDA5clVtSktORkpPSzAxbVNYSnhjRmRrUTNvNU9WWlBTV1JrUlRaUU1FRnNNMjByVUROR1RVOUdSazlzTUZaaWFrMHpZaXRZTm5wemQwc3ZZa2RuTWtGNWFURmlaR1JuUTA1RWJsQkJkbVpDWlc5TlZpczBSelJ4ZWtWTGVHSkxUVmMwUWxSTVlXbGFVMHg0VTA1ME1uTnhNVXRPUzI4NVowVndURW80V0ZObmFFMDJia3hQTkZWMFNWUk5ZemszUkRGV1ZrbERTR0ZLS3pOSFdrVlJibTlWWmpGNWFqaFdSRkJvZFRSblR5OVZTRTQzYVZKNlRVdHBaREpCU0hoNFpqaHlZME5HVW0xUVlXeG1NazFtTUdaMFkySldjbTFCUVdvdk5XSXJha1J1WlVscGNrMU9TM1paTmxsaFlYbDJOemhsVldoRVR5czJhRFJTWlZOUE9FWXdkMjk1TUZkdWVGVnBjRmRCWVZkMksyUlFkMEk0U1RObGVuY3ljRVEzTlV4eVptWm1ObTgzTlhwcFREaE9hVll4VVhoNmQzUjFkbGt5U0VST0sweEdWMDFuSzFZck5DOU5LMFZLYldSWVpuTnhNazV6VG1adlRISkVkMFJYVjFWaFVrc3pLMHRQU25sMlVXMWlaM0ZCZUdsNmExbFRlV3Q0TmpoVU5FMHlZa1F4TW1SYVVsZ3ZMME5NWWtsNGFrZGtUa1ZzY1hKdU1FRXljVGhWYkRkT2NFMU9aa0pXWmpKMloxcGlabkY1WldGeWVpOVNka3N3V1cxNldscHJPVzluVFVkb1oxRldTemwyUjA1NWEySnBPVEE1VVhsWVVVUnFkVmhoT0hKM09EaEdLMHhYTWs1V05HSlFjbFpNYVdSeU1YZENiV1I0T1dSaU0waEpTalp2Vm1jeVlrWmtSbVp2Y0VRemFXNVlNMmd4WkRoek0xbE5aVlJxZG1OdldXNUxiRVEyTkRsTmExWnViVGN2UkcxSVpFOXFUbU0wZFZGMFZUYzBZUzgyVUZGVmJqRkdaVmczSzBGalRuQnJUekpCYkcwNU1FNVllWGhNV1dFelQzQXpUa1ZDYTAxdE9Ib3JWRVZvU25OWE1XeFFhMnA2U1ZwblIycE9LMlV3WmpGS2NXbFpTa2xRY2xoVU1FaDNTR2QzTTFsR05HbHVOMWRXUm5KcFpESm5lRUZhUWxSNFpXOW1RME5IVjNGeVQwSk9RVWxhY0ROQk1GaGxXVTFVVDBremEzcHRkbkpuUkdwbFRYSndUemhhWmtGRk9FSTVjMjlzY2tKdGRUSTBPSGxzTXpBMGFsUXJOemhaYUZKdlNURXZTbFZGZFhWMFMyZGlVbEYzT0VnemFtMXRZa05yUm0weE1YWmliMlZQUjB0WFdWZHNjMFZ1UkVKb1RtWk5VVUZtUmtSbU1GWnhkakUxWm1Gb2JWZGhlVU15VGxCVmMzWjVhVkZhTVZKSmEyRmtTMDVNUnpSUFJFNTVkRm94VXpsdk4wNW9aMUpyYmtaelJXazRlRWt6T0ZWRFExUnpRMlZFUm5sdVdIbEZTMGd5WlVabk9GSlhka1l3TDNZNVNYTm5Na2xMYVhsQldYbEZkakV2YjNwNVNuaGhSa3R6VlZScVdUWm5aVE42ZG1kalFWUkhOM052U1dkS1p6SlRWamMyVEV4RVFtVlFWMUZWU0d0dU1uRkhhVlUzU1VaVWFWSnJaemhpUTA1aWMyeG9RMWgxVnl0aE4xSm1TMWh2TWxCd1ZrWlBSVlZsZWs1elQzSjBZbTlWV1VFNVRUbFFXbmQ1UzJ4MGQyWjVNa3hqTkhOM2FVeENkbUZHUkZWTFpVZGFSako0VEd0cGRWTm9MelJXZDFSVE5WaE5UekZSV0ZwRGFrUkliVTEwVkZjMU0wWXphMkU1TlRCMk9XSXJaMGxqVGtwaVUyaGtVREpqVDFZMFEyTkVSVXB2V1U5TWFTdEpNa2R5YTNGWk0yWklkVGxUVjBwTVMyWlBhR3hFU1RZeFZGcG9lVlZYV0V4M1RuRmFhMjFrTmxZMkx6UnFNbUZJWnpCR2RqVkhiek50YjFreFdHRjVRVmRTWjNwNVUyZFpabE56TWpadlQzbFhTakZPVTBKSlJYTkxWMmhLYjNaNUwxaG5hSEpTYUVOWWRWQnJjMDltYm5sMVFTdG5helpLUlhKdVp6TkVkbTVaZG5rMlFsWmtaV2hXTTI5cE1YSjJUblJqUVZrelpEZFViblZyVjBWRWVERmFkVlUzYUdweFRrRk5NRzAxTDI1dk5ETndjRlJUVVZnek4wdEtiSFZ3U1ROUVNqSnZTbEpoYkhoYVdWZFVhRk0xTWtaSFdpOVphRmhVUzJ0a1IwaHRWRVp4YlZrME5tVmlMMWxoZURGeWRXazRNSEJIUkhwbFFrWjZMMlpyV0dwdFMxbzFPWG92UTJaTkx6Sk9XbloyVFM4NVZXbFZNRzk0SzNnclNuSkxXVEJEVjFoMGNqTTRjMVpyVFRORGJHTnBRa292VlU4eWFtWjNVelJDZWxjeVJXRmhSa2RoTjAwNFkwVlVibmh3TVZkTksyaHhWUzlNT1M4NVVteGxiVGhQY2pCVldsTmhOMmQ0TDBobVVuVm5aRUY0UlRGbFZVSktWWFZSV0VOQ1JqRlRRbGxxWVVkT1RXOTBTa3htTkhOM0szZzVVeXRzZWxKNlR6TnBlR1F3TWpWeE4yaG9jMU5hUXk4cmFuUnRWVGh4ZFZsRGRtTk5hbGgzVVVoWWVXbEZjMXA2VkRkU2RYcEpZbXBhVDFJMWVrTXliR2wxVTFoaGJIQkhhV1ZwVURGelpYTTRhRXRHVUZKRmRWazNUVmxFYlhSc1NHWTRSV0ZEUldrek0xTmpjR2t6T0dsUE9XcEVhRmRFUTNSaWRIRk5SbU5ZYUc1bWJEVktabWhGVWpGNlpFZ3ZZVFpCWVNzeFMxcFRRWGROZWtwbGNXUjZRMWhyZDA1cmFVcHlialZDVjNwc1VrZE1iRk4wUzJOaGRTODJXR1F3ZVV0UFJqaG5abXRqWmtWR1VXVjBORlJwY0dKcEwyWTRkRGxJTlRNeWNXaGxkRVF6ZEZkemExUjFVelV3VFVZNUwzVXdiMVp4ZFZrdmRYTkZaRE5oUWtwQmRYSkpablZaWlhGNGVrUmhaR1p0YlZGTk1WRndTbVZqVVVKcGVEa3dhV3BvVHl0WGVHdDZOR0YyWWpOTlZ6RnVVRkl2ZVZCVGJFUXlaV1pFZEM5MVRXa3JRM2hXZDFjMFZTdHdhRUpUYjJkTkswZFhSbmt2VjJveVRVYzBhMGhyTDI4MlFsWTRValZOTkdNdlRVTklUaTl5WkZKV1ZIaG9iMFF6TTBoUU5UUlNZVFZoTm00MEt6STRhM3BaZGtwa2RraDROWE5ESzFkaFpsZE1aVmhSV1U5TU9HNXdZbGRMTlVsYWNFOU5jbVp2Tm5aWlMwaDNRVU5WWjNONVdXNU1ZMDFJY0ZOcmFHeEJORmQ1WkU1YVFXSTVjVzQxVTA5M2JtVXpNWFpNVTIwcldVeFhTWFJrWkhJMGVreE5XRlJRYlhkMFUzaEpXSEpQT0hkUFZtdExTVDAueFFyTll5cFJpb1VPeWxibkdZeVpLcUxMMmtTTHowZHVoTmx1NG1oT2VnSU95VUR4TTY4ZUlMeGl4dGstMlpONk56ZV9jUWM1UTJ6dDFYY1FiaVBLOHc=",
    'encrypted': 'true',
    '_eventId': 'submit',
    'loginType': '1',
    'submit': '登 录'
}
if __name__ == "__main__":
    ahau_url = "https://www.ahau.edu.cn/"
    my_url = "http://ids.ahau.edu.cn/cas/login?service=http%3A%2F%2Fi.ahau.edu.cn%2F_web%2Ffusionportal%2Findex.jsp%3F_p%3DYXM9MSZwPTEmbT1OJg__"
    xinxi = 'http://oa.ahau.edu.cn/info/inforead/infolist.shtml?e_id=1'
    all_titles = []
    all_urls = []
    all_urls.append(ahau_url)
    ahau_html = get_html(ahau_url)
    # get_data(ahau_html)
    get_data(ahau_html)
    for i in range(len(all_urls)):
        sql = "insert into ss_ahau(title,url) VALUES ('%s','%s');" % (all_titles[i], all_urls[i])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行1
            db.commit()
        except:
            # 如果发生错误则回滚
            db.rollback()
    # print(all_titles)
    # print(all_urls)
    # for s in ls_urls:
    #     if s not in all_urls:
    #         all_urls.append(s)
    # all_titles.append(get_title(ahau_html, all_titles))
    # get_all1(all_urls, all_titles)
    # i = 0
    # for t in all_titles:
    #     i = i+1
    #     print(t)
    # print(i)
