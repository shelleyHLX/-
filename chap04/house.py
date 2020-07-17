# coding: utf-8
# Author: shelley
# 2020/7/1419:23
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions
import unittest, time, re
import pandas as pd


class MyCrawler(object):
    def __init__(self):
        self.path = "./data"

        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.driver = webdriver.Firefox()
        self.base_url = "http://data.house.163.com/bj/housing/trend/district/todayprice/{date:s}/{interval:s}/allDistrict/1.html?districtname={disname:s}#stoppoint"
        self.data = None

    def craw_page(self, date="2014.01.01-2018.09.15", interval="month", disname="全市"):
        driver = self.driver
        url = self.base_url.format(date=date, interval=interval, disname=disname)
        print('访问网址：' + url)
        driver.get(url)

        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "resultdiv_1")))

            print(driver.title)

            self.data = pd.DataFrame()

            ct = True
            while ct:
                self.get_items_in_page(driver)

                e_pages = driver.find_elements_by_xpath(
                    '//div[@class="pager_box"]/a[@class="pager_b current"]/following::a[@class="pager_b "]')

                if len(e_pages) > 0:
                    next_page_num = e_pages[0].text
                    e_pages[0].click()

                    # 通过判断当前页是否为我们点击页面的方式来等待页面加载完成
                    WebDriverWait(driver, 10).until(
                        expected_conditions.text_to_be_present_in_element(
                            (By.XPATH, '//a[@class="pager_b current"]'),
                            next_page_num
                        )
                    )

                else:
                    ct = False
                    break

            return self.data

        finally:
            driver.quit()

    def get_items_in_page(self, driver):
        e_tr = driver.find_elements_by_xpath("//tr[normalize-space(@class)='mBg1' or normalize-space(@class)='mBg2']")
        temp = pd.DataFrame(e_tr, columns=['web'])
        temp['时间'] = temp.web.apply(lambda x: x.find_element_by_class_name('wd2').text.split(' ')[0])
        temp['套数'] = temp.web.apply(lambda x: x.find_element_by_class_name('wd5').text)
        temp['均价'] = temp.web.apply(lambda x: x.find_element_by_class_name('wd7').text)
        temp['去化'] = temp.web.apply(lambda x: x.find_element_by_class_name('wd14').text)
        del temp['web']

        self.data = pd.concat([temp, self.data], axis=0)


mcraw = MyCrawler()
data = mcraw.craw_page()
print(data)

data= data.sort_values(by='时间')
print(data.to_string(index=False))
data.to_csv('./data/housing_beijing.csv',index=False, encoding='utf-8')
data.to_csv()

import matplotlib.pyplot as plt

# 指定默认字体
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['font.family']='sans-serif'
# 用来正常显示负号
plt.rcParams['axes.unicode_minus']=False

data = pd.read_csv('./data/housing_beijing.csv')
y = [float(s.replace(',','')) for s in data['均价'].values]
plt.plot(y,color='red', marker='o', linestyle='solid')
plt.xlabel(u'日期')
plt.ylabel(u'均价(元)')
plt.title(u'北京房价走势')
plt.show()


"""
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xbc in position 2: invalid start byte


"""