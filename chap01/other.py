# coding: utf-8
# Author: shelley
# 2020/7/717:21
import re

from bs4 import BeautifulSoup

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""
doc = """
<html>
<head>
   <meta charset="utf-8" />
   <meta http-equiv="X-UA-Compatible" content="IE=edge">
   <title>Page Title</title>
</head>
<body>
   <div class='main-page'>
       <ul class='menu-list'>
               <li>首页</li>
               <li>新闻</li>
               <li>影视</li>
       </ul>
   </div>
</body>
</html>
"""
# 创建一个BeautifulSoup解析对象
soup = BeautifulSoup(doc, "html.parser", from_encoding="utf-8")
# 获取所有的链接
links = soup.find_all('div')
print("所有的链接")

for link in links:
    print(link.name, link['href'], link.get_text())

print("获取特定的URL地址")

link_node = soup.find('a', href="http://example.com/elsie")
print(link_node.name, link_node['href'], link_node['class'], link_node.get_text())


print("正则表达式匹配")

link_node = soup.find('a', href=re.compile(r"ti"))
print(link_node.name, link_node['href'], link_node['class'], link_node.get_text())

print("获取P段落的文字")

p_node = soup.find('p', class_='story')
print(p_node.name, p_node['class'], p_node.get_text())
