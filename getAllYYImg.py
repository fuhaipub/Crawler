import re
import urllib.request
import urllib
import http.cookiejar
import sys
sys.path.append("C:\\pyProject\\Crawler")
from Crawler.getYYImgMore import downloadMoreImg
from io import StringIO, BytesIO
from lxml import etree
from urllib import request
from urllib.parse import urlparse

from collections import deque

# head: dict of header
def makeMyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

logfilename="crawler_wwwYYcom.log"
imgPath="C:\\pyProject\\Crawler\\img\\"
imgPathGood="C:\\pyProject\\Crawler\\img_good\\"
#urlDataFile="urldata.txt"

fsLog=open(logfilename,'w',encoding='utf-8')
#fsData=open(urlDataFile,'w',encoding='utf-8')

queue = deque()
visited = set()

ImgDownloaded = set()

url ='http://www.yy.com'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()  # 队首元素出队
    visited |= {url}  # 标记为已访问

    #log= 'Get URL: ' + str(cnt) + ' Getting<---  ' + url
    #fsLog.write(log+'\n')
    #print (log)
    cnt += 1

    oper = makeMyOpener()
    try:
        urlop = oper.open(url, timeout=3)
        #urlop = urllib.request.urlopen(url,timeout=2)
        if 'html' not in urlop.getheader('Content-Type'):
            continue
        data = urlop.read().decode('utf-8')

        downloadMoreImg(data, imgPathGood)

        #解析html
        parser = etree.HTMLParser()
        tree= etree.parse(StringIO(data), parser)
        imghrefs=['http:'+img for img in tree.xpath("//img/@data-original") if img and img.strip() !="" and img[0:4] != 'http' ]

        #把“更多”的链接也加入到imghrefs中
        #如果发现页面里有符合
        #---------------------------------

        index=0
        for imgurl in imghrefs:

            imgName = urlparse(imgurl).path.split('/')[-1]
            if imgName[-4:] != ".jpg" :
                #print ("不是jpg文件不下载，跳过...%s" % imgName)
                continue

            if imgName in ImgDownloaded:
                print ("文件已经下载，跳过...%s" % imgName)
                continue

            imgfilename=imgPath+imgName
            #下载文件
            request.urlretrieve(imgurl, imgfilename)
            print("下载图片:%s" % imgurl)
            #标记文件已经被下载
            ImgDownloaded |={imgName}

            index+=1
        #fsData.write(data)
    except Exception as e:
        print(e)
        continue

    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data):
        #if 'http' in x and x not in visited and  '.yy.com' in x:
        if x in visited:
            continue

        if x[0:4] == "http" and "yy.com" not in x and 'dwstatic.com' not in x:
            continue
        elif x[0:2] =="//":
            x="http:"+ x
        elif x[0] =="/":
               x="http://www.yy.com"+ x

        queue.append(x)
        #log='Add URL Queue--->  ' + x +'Queue length=' +str(len(queue))
        #fsLog.write(log+'\n')
        #print (log)