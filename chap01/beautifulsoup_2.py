# coding: utf-8
# Author: shelley
# 2020/7/717:14
#-*-coding:utf-8-*-
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

#创建beautifulsoup对象
#也可以用打开本地的html文件来创建beautifulsoup对象，例如:
soup = BeautifulSoup(open('index.html'))
# soup = BeautifulSoup(html)

#格式化输出
print (soup.prettify())
