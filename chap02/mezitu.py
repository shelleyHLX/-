# coding: utf-8
# Author: shelley
# 2020/7/717:28


import requests
import os
import time
from bs4 import BeautifulSoup
"""
beautifulsoup4 (4.6.0)

"""

def download_page(url):
   '''
   用于下载页面
   '''
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
   r = requests.get(url, headers=headers)
   r.encoding = 'GBK'
   return r.text


def get_pic_list(html):
   '''
   获取每个页面的套图列表,之后循环调用get_pic函数获取图片
   '''
   soup = BeautifulSoup(html, 'html.parser')
   pic_list = soup.find_all('li', class_='wp-item')
   for i in pic_list:
       a_tag = i.find('h3', class_='tit').find('a')
       link = a_tag.get('href')  # 获得一张图片的链接
       text = a_tag.get_text()  # 获得一张图片的文字
       get_pic(link, text)


def get_pic(link, text):
   '''
   获取当前页面的图片,并保存
   '''
   html = download_page(link)  # 下载界面
   soup = BeautifulSoup(html, 'html.parser')
   pic_list = soup.find('div', id="picture").find_all('img')  # 找到界面所有图片
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
   create_dir('pic/{}'.format(text))
   print('pic/{}'.format(text))
   for i in pic_list:
       pic_link = i.get('src')  # 拿到图片的具体 url
       print('pic_link', pic_link)

       r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
       with open('pic/{}/{}'.format(text, pic_link.split('/')[-1]), 'wb') as f:
           f.write(r.content)
           time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封
       # exit(0)

def create_dir(name):
   if not os.path.exists(name):
       os.makedirs(name)


def execute(url):
   page_html = download_page(url)
   # print(page_html)
   # exit(0)
   get_pic_list(page_html)


def main():
   # create_dir('pic')
   # queue = [i for i in range(1, 10)]   # 构造 url 链接 页码。
   # threads = []
   # while len(queue) > 0:
   #     for thread in threads:
   #         if not thread.is_alive():
   #             threads.remove(thread)
   #     while len(threads) < 2 and len(queue) > 0:   # 最大线程数设置为 5
   #         cur_page = queue.pop(0)
   #         url = 'https://www.meizitu.com/a/qingchun_3_{}.html'.format(cur_page)
   #         thread = threading.Thread(target=execute, args=(url,))
   #         thread.setDaemon(True)
   #         thread.start()
   #         print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
   #         threads.append(thread)

   create_dir('pic')
   for page in range(1,10):
       url = 'https://www.meizitu.com/a/qingchun_3_{}.html'.format(page)
       execute(url)
       print('正在下载{}页'.format(page))


if __name__ == '__main__':
   main()


