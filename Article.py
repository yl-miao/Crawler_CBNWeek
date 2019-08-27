import pickle
import re
import time
import requests
from requests import exceptions
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import logging

logger = logging.getLogger()
logger.setLevel('INFO')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('DEBUG')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('articleLogs.log')  # 输出到文件的handler
fhlr.setFormatter(formatter)
fhlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
logger.addHandler(chlr)
logger.addHandler(fhlr)

chrome_options = Options()
chrome_options.add_argument("--headless")  # define headless
loginUrl = 'https://www.cbnweek.com/account/login?next=%2F'
# url = "https://www.cbnweek.com/articles/magazine/23235"
chromePath = r'E:\chromedriver.exe'
headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.cbnweek.com/read",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
}
wd = webdriver.Chrome(executable_path=chromePath, options=chrome_options)  # 构建浏览器
cookies = {}
html = ""
s = requests.Session()
cnt = 0


def getCookie():
    global cnt

    logger.info("正在更新cookie")
    wd.get(loginUrl)
    wd.find_element_by_name("username").click()
    wd.find_element_by_name("username").clear()
    wd.find_element_by_name("username").send_keys("13256900366")
    wd.find_element_by_name("password").click()
    wd.find_element_by_name("password").clear()
    wd.find_element_by_name("password").send_keys("yl200099")
    wd.find_element_by_xpath("//button[@type='submit']").click()
    logger.info("正在等待cookie加载")
    time.sleep(18)
    cookies = wd.get_cookies()  # 导出cookie
    pickle.dump(cookies, open("cookies.pkl", "wb"))  # 保存cookies
    logger.info("保存新cookie完毕")
    cnt = cnt + 1


def init():
    pass


def getCnt():
    return cnt


def getParas(urll):
    url = urll
    s.cookies.clear()
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    s.headers.update(headers)
    r = s.get(url, timeout=20)
    if r.status_code != 200:
        logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
    r.encoding = 'utf-8'
    html = r.text
    if (html.find("使用订阅账号可在周刊网站、APP享受相同权益") != -1 and html.find("订阅后可阅读周刊自创刊以来的全部杂志数字版") != -1 and html.find(
            "每周四先于纸刊发行，提前阅读杂志内容") != -1):
        logger.info("cookies失效！正在爬：" + url)
        getCookie()
        s.cookies.clear()
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        s.headers.update(headers)
        test = s.get(url, timeout=20)
        if test.status_code != 200:
            logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
        test.encoding = 'utf-8'
        html = test.text
        paras = re.findall(r'<p>(.*?)</p>', html, re.I | re.S | re.M)
        pickle.dump(paras, open("paras.pkl", "wb"))  # 保存paras
    else:
        paras = re.findall(r'<p>(.*?)</p>', html, re.I | re.S | re.M)
        pickle.dump(paras, open("paras.pkl", "wb"))  # 保存paras


def getSummary(urll):
    url = urll
    s.cookies.clear()
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    s.headers.update(headers)
    r = s.get(url, timeout=20)
    if r.status_code != 200:
        logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
    r.encoding = 'utf-8'
    html = r.text
    if (html.find("使用订阅账号可在周刊网站、APP享受相同权益") != -1 and html.find("订阅后可阅读周刊自创刊以来的全部杂志数字版") != -1 and html.find(
            "每周四先于纸刊发行，提前阅读杂志内容") != -1):
        logger.info("cookies失效！")
        getCookie()
        s.cookies.clear()
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        s.headers.update(headers)
        test = s.get(url, timeout=20)
        if test.status_code != 200:
            logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
        test.encoding = 'utf-8'
        html = test.text
        summary = re.findall(r'<div class=\"article-summary text-muted\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(summary, open("summary.pkl", "wb"))  # 保存summary
    else:
        summary = re.findall(r'<div class=\"article-summary text-muted\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(summary, open("summary.pkl", "wb"))  # 保存summary


def getNote(urll):
    url = urll
    s.cookies.clear()
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    s.headers.update(headers)
    r = s.get(url, timeout=20)
    if r.status_code != 200:
        logger.warning('crawling url:' + url + ', status code is: ' + str(r.status_code))
    r.encoding = 'utf-8'
    html = r.text
    if (html.find("使用订阅账号可在周刊网站、APP享受相同权益") != -1 and html.find("订阅后可阅读周刊自创刊以来的全部杂志数字版") != -1 and html.find(
            "每周四先于纸刊发行，提前阅读杂志内容") != -1) or (
            html.find("您正频繁刷新") != -1 and html.find("请稍后再试") != -1):  # 好像是 您正频繁刷新，请稍后再试
        logger.info("cookies失效！正在爬：" + url)
        getCookie()
        s.cookies.clear()
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        s.headers.update(headers)
        test = s.get(url, timeout=20)
        if test.status_code != 200:
            logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
        test.encoding = 'utf-8'
        html = test.text
        note = re.findall(r'<div class=\"article-content\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(note, open("note.pkl", "wb"))  # 保存notes
        img_url = re.findall(r"(?<=img src=\").+?(?=\")", note[0], re.I | re.S | re.M)
        pickle.dump(img_url, open("img_url.pkl", "wb"))  # 保存img_url
        summary = re.findall(r'<div class=\"article-summary text-muted\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(summary, open("summary.pkl", "wb"))  # 保存summary
    else:
        note = re.findall(r'<div class=\"article-content\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(note, open("note.pkl", "wb"))  # 保存notes
        img_url = re.findall(r"(?<=img src=\").+?(?=\")", note[0], re.I | re.S | re.M)
        pickle.dump(img_url, open("img_url.pkl", "wb"))  # 保存img_url
        summary = re.findall(r'<div class=\"article-summary text-muted\">(.*?)</div>', html, re.I | re.S | re.M)
        pickle.dump(summary, open("summary.pkl", "wb"))  # 保存summary
