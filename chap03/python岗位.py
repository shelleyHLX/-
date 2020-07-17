import random
import time

import requests
from openpyxl import Workbook

import pymysql.cursors

"""
lagou网爬取
"""

def get_conn():
   '''建立数据库连接'''
   conn = pymysql.connect(host='localhost',
                               user='root',
                               password='123456',
                               db='python_job',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
   return conn


def insert(conn, info):
   '''数据写入数据库'''
   with conn.cursor() as cursor:
       sql = "INSERT INTO python_jobs (shortname, fullname, industryfield, companySize, salary, city, education) VALUES (%s, %s, %s, %s, %s, %s, %s)"
       cursor.execute(sql, info)
   conn.commit()


header = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}


def get_json(url, page, lang_name, s, cookie):
   '''返回当前页面的信息列表'''

   data = {'first': 'false', 'pn': page, 'kd': lang_name}
   json = s.post(url, data=data, headers=header, cookies=cookie, timeout=5).json()

   print(json)

   list_con = json['content']['positionResult']['result']
   info_list = []
   for i in list_con:
       info = []
       info.append(i.get('companyShortName', '无'))  # 公司名
       info.append(i.get('companyFullName', '无'))
       info.append(i.get('industryField', '无'))   # 行业领域
       info.append(i.get('companySize', '无'))  # 公司规模
       info.append(i.get('salary', '无'))   # 薪资
       info.append(i.get('city', '无'))
       info.append(i.get('education', '无'))   # 学历
       info_list.append(info)
   return info_list   # 返回列表


def main():
   lang_name = 'python'
   wb = Workbook()  # 打开 excel 工作簿
   conn = get_conn()  # 建立数据库连接  不存数据库 注释此行

   urls = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='

   s = requests.Session()
   # 获取搜索页的cookies
   s.get(urls, headers=header, timeout=3)
   # 为此次获取的cookies
   cookie = s.cookies

   page = 1
   ws1 = wb.active
   ws1.title = lang_name

   url = 'https://www.lagou.com/jobs/positionAjax.json?city=广州&needAddtionalResult=false'

   while page < 31:   # 每个城市30页信息
       print('url', url)
       # exit(0)
       info = get_json(url, page, lang_name, s, cookie)
       page += 1
       time.sleep(random.randint(10, 20))
       for row in info:
           insert(conn, tuple(row))  # 插入数据库，若不想存入 注释此行
           ws1.append(row)
   conn.close()  # 关闭数据库连接，不存数据库 注释此行
   wb.save('{}职位信息.xlsx'.format(lang_name))

if __name__ == '__main__':
   main()



"""
hlx2@NLP:~/桌面$ sudo service mysql start

hlx2@NLP:~/桌面$ mysql -u root -p

数据库：
CREATE DATABASE python_job;
use python_job;
CREATE TABLE python_jobs(shortname text(2000),fullname text(2000),industryfield text(2000),companySize text(2000),salary text(2000),city text(2000),education text(2000));
"INSERT INTO python_jobs (shortname, fullname, industryfield, companySize, salary, city, education) VALUES (%s, %s, %s, %s, %s, %s, %s)"
"""



"""
{"POST":{"scheme":"https","host":"www.lagou.com","filename":"/jobs/positionAjax.json",
"query":{"city":"广州","needAddtionalResult":"false"},"remote":{"地址":"117.50.39.99:443"}}}
"""



"""
解决方法：运行命令   mysql> alter table 表名 convert to character set utf8mb4;
pymysql.err.InternalError: (1366, "Incorrect string value: '\\xE7\\x9C\\x81\\xE7\\x9C\\x81...' for column 'shortname' at row 1")
"""

