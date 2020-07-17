# coding: utf-8

import requests

# url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
url='https://www.lagou.com/jobs/positionAjax.json?city=广州&needAddtionalResult=false'
payload = {
    'first': 'true',
    'pn': '1',
    'kd': '自然语言处理'
}

"""
Referer: https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=

"""
header = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
    'Accept': 'application/json, text/javascript, */*; q=0.01'
}
urls = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
# urls = 'https://www.lagou.com/jobs/list_%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86?city=%E5%B9%BF%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput='
s = requests.Session()
# 获取搜索页的cookies
s.get(urls, headers=header, timeout=3)
# 为此次获取的cookies
cookie = s.cookies
# 获取此次文本
response = s.post(url, data=payload, headers=header, cookies=cookie, timeout=5).json()
print(type(response))
# print(response)
# print(type(response))
# import json
# dicts = json.loads(response)
# print(type(dicts))
# for k, v in dicts.items():
#     print(k, v)
# print(dicts.keys())
list_con = response['content']['positionResult']['result']
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

print(info_list)