# coding: utf-8
# Author: shelley
# 2020/7/1417:28
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('https://www.baidu.com/')
search_input = driver.find_element_by_id("kw") # 获取到百度搜索框
search_input.send_keys("刘亦菲")  # 自动输入 刘亦菲
submit = driver.find_element_by_id("su")  # 获取到百度一下按钮
submit.click()  # 点击搜索


"""
pip install selenium

文档：
https://selenium-python-zh.readthedocs.io/en/latest/index.html

"""

"""
查看浏览器版本：
1.打开“谷歌浏览器”，点击右上角“三个点”。
2.选择“帮助”选项，点击“关于Google Chrome”。
3.进入界面后即可看到谷歌浏览器版本。
"""

"""
谷歌浏览器版本不对：
问题：selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 81

各种浏览器版本对应的driver版本。
http://npm.taobao.org/mirrors/chromedriver/

"""
