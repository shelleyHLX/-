# coding: utf-8
# Author: shelley
# 2020/7/717:04
from bs4 import BeautifulSoup

# print(help(BeautifulSoup))
# exit(0)
context = open('example.html', encoding='utf-8').readlines()
context = ''.join(context)
print(context)
soup = BeautifulSoup(context, 'html.parser',from_encoding="utf-8") #加载我们的html文件
print(soup.find('div'))  # 找到 div 标签



