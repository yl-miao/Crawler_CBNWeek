# Crawler_CBNWeek
a crawler to crawl CBNWeek magazines and generate PDFs suitable to be read on a 6-inch kindle like kpw3,kpw4

This is not a pirating program and shall not be used with piracy purposes. This only works when you have an official CBNWeek account that can access paid subscriptions of CBNWeek.

爬取网页版的第一财经周刊并自动生成适合6英寸屏幕的kindle，如kpw3，kpw4的PDF。

请勿用作盗版用途，使用时需要有已经付费订阅第一财经周刊电子版的账户。本程序的目的只是方便的自动爬取该杂志并产生适合在kindle上看的PDF

使用
在Article.py中填入账号和密码

在main.py中将注释取消，并将注释段下面的一段注释掉，这一段是方便下次开启程序后接着上一次继续爬

运行main.py，程序会在运行目录创建books文件夹，从2019年爬到2018年，调试信息会输出在命令行，各个部分的调试信息会自动写入(追加模式)mainLogs.log listLogs.log articleLogs.log中。生成文件的命名格式如：NO.536-“云上”贵州-2019.1.25.pdf 生成的PDF是按照6英寸的kindle屏幕优化的，生成样例在 theme-中国新式茶饮行业十大品质严选金字招牌.pdf这里。(theme开头代表该期本来就是免费的，所以就用这期免费的做演示了)

要爬取某期单期的话可以自己写一个类似的脚本直接调用List.py:

import List

List.get("需要爬的那期的链接", "可以自定义存储目录")#注意链接最后的数字和该期编号一般不对应
说明
main.py是从阅读页面中得到每年各期的链接，List.py负责调用Article.py来将一整期的杂志输出。

使用selenium获得cookies传入requests库，使用正则表达式得到内容再生成一个html，最后调用pdfkit生成pdf
