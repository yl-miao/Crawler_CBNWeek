import re
import time
import requests
import pickle
import pdfkit
from requests import exceptions
import Article
import os
import logging
import List
import os
import time

logger = logging.getLogger()
logger.setLevel('INFO')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('DEBUG')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('mainLogs.log')  # 输出到文件的handler
fhlr.setFormatter(formatter)
fhlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
logger.addHandler(chlr)
logger.addHandler(fhlr)

url = "https://www.cbnweek.com/magazine/527"
art_headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.cbnweek.com/read",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
}

for i in range(0,12):# 2019-i 即为2019年到2009年
    logger.info("正在爬取"+str(2019-i)+"年的书籍")
    path=os.getcwd()+'\\books\\'+str(2019-i)
    if not os.path.exists(path):
        os.makedirs(path)
    savePath=path+'\\'
    url="https://www.cbnweek.com/read?year="+str(2019-i)+"&type=all"
    r = requests.get(url, headers=art_headers, timeout=15)
    r.encoding = 'utf-8'
    html = r.text
    urls = re.findall(r"(?<=a class=\"top-cover-image\" href=\").+?(?=\")", html, re.I | re.S | re.M)
    urls.extend(re.findall(r"(?<=a class=\"content-item-wrapper\" href=\").+?(?=\")", html, re.I | re.S | re.M))
    for i in range(0, len(urls)):
        urls[i] = "https://www.cbnweek.com" + urls[i]
        logger.info("发现杂志："+urls[i])

    for i in range(0,len(urls)):
        logger.info("正在爬取"+urls[i])
        time.sleep(5)
        List.getList(urls[i],savePath)

'''
for i in range(1, 12):  # 2019-i 即为2019年到2009年
    logger.info("正在爬取" + str(2019 - i) + "年的书籍")
    path = os.getcwd() + '\\books\\' + str(2019 - i)
    if not os.path.exists(path):
        os.makedirs(path)
    savePath = path + '\\'
    url = "https://www.cbnweek.com/read?year=" + str(2019 - i) + "&type=all"
    r = requests.get(url, headers=art_headers, timeout=20)
    r.encoding = 'utf-8'
    html = r.text
    urls = re.findall(r"(?<=a class=\"top-cover-image\" href=\").+?(?=\")", html, re.I | re.S | re.M)
    urls.extend(re.findall(r"(?<=a class=\"content-item-wrapper\" href=\").+?(?=\")", html, re.I | re.S | re.M))
    for j in range(0, len(urls)):
        urls[j] = "https://www.cbnweek.com" + urls[j]
        logger.info("发现杂志：" + urls[j])
    if i == 1:
        for j in range(13, len(urls)):
            logger.info("正在爬取页面：" + urls[j])
            time.sleep(6)
            List.getList(urls[j], savePath)
    else:
        for j in range(0, len(urls)):
            logger.info("正在爬取页面：" + urls[j])
            time.sleep(6)
            List.getList(urls[j], savePath)
'''