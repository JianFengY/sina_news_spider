'''
Created on 2018年1月22日

@author: Jeff Yang
'''

import requests
from urllib import request
from bs4 import BeautifulSoup
import xlwt


workbook = xlwt.Workbook()
worksheet = workbook.add_sheet('news.xls', cell_overwrite_ok=True)

worksheet.write(0, 0, label='标题')
worksheet.write(0, 1, label='地址')
worksheet.write(0, 2, label='时间')


def get_urls_and_titles():
    """获取新闻的url和标题"""
    start = 1
    for i in range(1, 1500):  # 表示前x页，但是跟网页显示的页数不一样，可以自己改
        # 这个url是一个api，里面有json格式的新闻信息，访问那个网页时在networks里面可以看到
        url = "http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=" + str(i)
        html = requests.get(url)
        content = html.json()
        print("页码："+str(i))
        for j in range(len(content['result']['data'])):  # 每一页新闻的信息条数
            news_title = content['result']['data'][j]['title']
            news_url = content['result']['data'][j]['url']
            news_time = get_time(news_url)
            print(news_title)
            print(news_url)
            print(news_time)
            worksheet.write(j + start, 0, label=news_title)
            worksheet.write(j + start, 1, label=news_url)
            worksheet.write(j + start, 2, label=news_time)
        start = start + len(content['result']['data'])


def get_time(url):
    """获取新闻的时间"""
    response = request.urlopen(url)
    content = response.read()
    soup = BeautifulSoup(content, 'html.parser')
    time = soup.find('span', class_="date")
    if time:
        return time.get_text()
    else:
        return None

get_urls_and_titles()

workbook.save('news.xls')
print("over")
