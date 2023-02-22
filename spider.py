# 爬取豆瓣Top250电影信息
import bs4
import re
import urllib.request
import urllib.error
import xlwt


# 创建正则表达式对象
findLink = re.compile(r'<a href="(.*)">')
findImgsrc = re.compile(r'<img.*src="(.*)" width="100"/>', re.S)   # re.S:换行符包括在内
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findNum = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 主函数
def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = "豆瓣电影Top250.xls"
    saveData(datalist, savepath)


def getData(baseurl):
    print("开始")
    datalist = []
    for i in range(0, 10):   # 每个网页有25部电影，需要循环10次
        url = baseurl + str(i*25)
        html = askURL(url)

        # 解析数据
        soup = bs4.BeautifulSoup(html, "html.parser")
        for item in soup.find_all('div', class_="item"):
            # print(item)    # 测试item
            data = []        # 保存一部电影的完整信息
            item = str(item)

            link = re.findall(findLink, item)[0]
            data.append(link)

            imgsrc = re.findall(findImgsrc, item)[0]
            data.append(imgsrc)

            # 部分电影有中英文名字
            titles = re.findall(findTitle, item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                etitle = titles[1].replace("/", "")     # 去除无关符号
                data.append(etitle)
            else:
                data.append(titles[0])
                data.append(" ")

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            num = re.findall(findNum, item)[0]
            data.append(num)

            # 部分电影没有概括
            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            # 相关内容里一些不必要的符号较多
            bd = re.findall(findBd, item)[0]
            bd = re.sub("<br(\s+)?/>(\s+)?", " ", bd)
            bd = re.sub("/", " ", bd)
            data.append(bd.strip())        # 去掉空格

            datalist.append(data)

    # print(datalist) # 测试datalist
    return datalist


# 获得一个URL的网页内容
def askURL(url):
    # 模拟浏览器头部信息，向服务器发送消息(该信息需要自己获得)
    print("爬取中...")
    head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50"}
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


# 保存数据到excel
def saveData(datalist, savepath):
    print("保存中...")
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet("豆瓣电影Top250", cell_overwrite_ok=True)  # 创建工作表(可覆盖)
    col = ("电影详情链接", "图片链接", "中文名", "英文名", "评分", "评价数", "概括", "相关信息")
    # 创建列名
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    # 保存数据
    for i in range(0, 250):
        # print("第%d部" % (i+1))
        data = datalist[i]
        for j in range(0, 8):
            sheet.write(i+1, j, data[j])

    book.save("豆瓣电影Top250.xls")
    print("完成")


if __name__ == "__main__":
    main()
















