import re
import time
import requests
import pickle
import pdfkit
from requests import exceptions
import Article
import os
import logging

logger = logging.getLogger()
logger.setLevel('INFO')
BASIC_FORMAT = "%(asctime)s:%(levelname)s:%(message)s"
DATE_FORMAT = '%m-%d %H:%M:%S'
formatter = logging.Formatter(BASIC_FORMAT, DATE_FORMAT)
chlr = logging.StreamHandler()  # 输出到控制台的handler
chlr.setFormatter(formatter)
chlr.setLevel('DEBUG')  # 也可以不设置，不设置就默认用logger的level
fhlr = logging.FileHandler('listLogs.log')  # 输出到文件的handler
fhlr.setFormatter(formatter)
fhlr.setLevel('INFO')  # 也可以不设置，不设置就默认用logger的level
logger.addHandler(chlr)
logger.addHandler(fhlr)

# print(Article.chromePath)
url = "https://www.cbnweek.com/magazine/527"
art_headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.cbnweek.com/read",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36"
}


def getList(urll, savePath):
    prep = u"<!doctype html>\n<html>\n<head><meta charset=\"UTF-8\"></head>\n<body>"

    prep.encode(encoding='utf-8')
    r = requests.get("https://www.baidu.com", headers=art_headers, timeout=20)
    url = urll
    try:
        r = requests.get(url, headers=art_headers, timeout=20)
        r.encoding = 'utf-8'
    except exceptions.HTTPError as e:
        logger.info(str(e))
    except exceptions.Timeout as e:
        logger.info(str(e))
    except exceptions.ConnectionError as e:
        logger.info(str(e))
        # time.sleep(3)
    except exceptions.ChunkedEncodingError as e:
        logger.info(str(e))

    html = r.text
    NoDate = re.findall(r'<div class=\"text-muted\">(.*?)</div>', html, re.I | re.S | re.M)
    ThisTitle = re.findall(r'<div class=\"aside-title-magazine PingFang-Semibold\">(.*?)</div>', html,
                           re.I | re.S | re.M)
    pcover = re.findall(r"<div class=\"magazine-cover full-size mb-3\">(.+?)</span>", html, re.I | re.S | re.M)
    cover = re.findall(r"(?<=img src=\").+?(?=\")", pcover[0], re.I | re.S | re.M)
    # logger.info("cover[0]:"+cover[0])
    prep += "<figure><img src=\"" + cover[0].rstrip(
        '400') + "2000" + "\"" + " width=\"510\"><figcaption></figcaption></figure>"
    logger.info('crawling url:' + url + ', status code is: ' + str(r.status_code))
    f = open(savePath + "temp.html", 'w', encoding="utf-8")
    titles = re.findall(r"<span class=\"article-item-title PingFang-Semibold\">(.+?)</span>", html, re.I | re.S | re.M)
    titles_url = re.findall(r"(?<=class=\"article-item-head\" href=\").+?(?=\")", html, re.I | re.S | re.M)
    pics = re.findall(r"background-image:url\((.+?)\)", html, re.I | re.S | re.M)
    t = []
    for i in range(0, len(pics)):
        if pics[i].find("imageView2/2/w/500") == -1:
            t.append(i)
    cnt = 0
    for x in t:
        logger.info(pics.pop(x - cnt))
        cnt = cnt + 1
    # Article.getCookie() 刚开始的时候要是cookies失效就把这行取消注释
    prep = prep + "<p>本期：" + ThisTitle[0] + "</p>"
    if len(NoDate) == 2:
        prep = prep + "<p>序号：" + NoDate[0] + " 出版日期：" + NoDate[1] + "</p>"
    else:
        prep = prep + "<p>本期是free的theme，文章数：" + NoDate[0] + "</p>"
    prep = prep + "<strong id=\"menu\">本期目录：</strong><br></br>"
    logger.info("生成目录中")
    for i in range(0, len(titles)):
        prep = prep + "<a href=\"#" + titles[i] + "\">" + titles[i] + "</a> " + "<br></br>"

    logger.info("目录生成完成，开始下载文章")
    for i in range(0, len(titles)):
        time.sleep(3.5)
        prep = prep + "<br></br><br></br><br></br>" + "<figure><img src=\"" + pics[i].rstrip(
            '500') + "2000" + "\"" + " width=\"382.5\"><figcaption></figcaption></figure>"
        logger.info("本期第" + str(i + 1) + "篇文章")
        prep = prep + "<strong" + " id=\"" + titles[i] + "\">" + "本期第" + str(i + 1) + "篇文章:"
        logger.info(titles[i])
        prep = prep + titles[i] + "</strong>"
        titles_url[i] = "https://www.cbnweek.com" + titles_url[i]
        Article.getNote(titles_url[i])
        summary = pickle.load(open("summary.pkl", "rb"))
        logger.info("本篇文章summary：")
        prep = prep + "<p> </p>" + "<i>" + "概要：" + summary[0] + "</i>" + "<p> </p><p> </p>"
        logger.info(summary[0])
        note = pickle.load(open("note.pkl", "rb"))
        img_url = pickle.load(open("img_url.pkl", "rb"))
        logger.info("本篇文章内容：")
        # prep = prep + "<i>" + "本篇文章内容：" + "</i>" + "<p> </p>"
        for i in range(0, len(img_url)):
            pos = note[0].find(img_url[i])
            lenn = len(img_url[i])
            str_list = list(note[0])
            str_list.insert(pos + lenn + 1, " width=\"382.5\"")
            note[0] = "".join(str_list)

        prep = prep + note[0] + "<p> </p>" + "<a href=\"#menu\">返回目录</a>" + "<br></br><br></br>"
        logger.info('*************************************************************************************')

    options = {
        'minimum-font-size': '26',
        'page-height': '3.5in',
        'page-width': '2.55in',
        'margin-top': '0.01in',
        'margin-right': '0.01in',
        'margin-left': '0.01in',
        'margin-bottom': '0.01in',
        'encoding': "UTF-8",
        'outline-depth': 10,
    }
    prep = prep + "</body>\n</html>"
    prep.encode(encoding='utf-8')
    f.write(prep)
    f.close()
    path_wkthmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
    logger.info("准备将加载的数据写入pdf文件")
    pdfkit.from_url(savePath + "temp.html", savePath + "out.pdf", configuration=config, options=options)
    Article.s.close()
    Article.wd.quit()
    # /:*?"<>| 去掉这些文件名不能含有的特殊符号
    ThisTitle[0] = ThisTitle[0].replace("\\", " ")
    ThisTitle[0] = ThisTitle[0].replace(":", " ")
    ThisTitle[0] = ThisTitle[0].replace("*", " ")
    ThisTitle[0] = ThisTitle[0].replace("?", " ")
    ThisTitle[0] = ThisTitle[0].replace("\"", " ")
    ThisTitle[0] = ThisTitle[0].replace("<", " ")
    ThisTitle[0] = ThisTitle[0].replace(">", " ")
    ThisTitle[0] = ThisTitle[0].replace("|", " ")
    if len(NoDate) == 2:
        outName = savePath + NoDate[0] + "-" + ThisTitle[0] + "-" + NoDate[1] + ".pdf"
    else:
        outName = savePath + "theme" + "-" + ThisTitle[0] + ".pdf"
    os.rename(savePath + "out.pdf", outName)
    logger.info("本次共更新cookies" + str(Article.getCnt()) + "次")
    logger.info("本次输出完成！输出文件名：" + outName)
