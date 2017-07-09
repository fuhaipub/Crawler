import re
import urllib.request
import urllib
import http.cookiejar
from io import StringIO, BytesIO
from lxml import etree
from urllib import request
import json
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

logfilename="crawler.log"
urlDataFile="test.htm"
imgPath='C:\\pyProject\\Crawler\\img\\'

fsLog=open(logfilename,'w',encoding="utf-8")
fsData=open(urlDataFile,'w',encoding="utf-8")

#url = 'http://www.hao123.com'  # 入口页面, 可以换成别的
url = 'http://www.yy.com/music/pop/more/476'

oper = makeMyOpener()
try:
    urlop = oper.open(url, timeout=3)
    #for key,value in urlop.getheaders():
    #    print(key + ":" +value)

    if 'html' not in urlop.getheader('Content-Type'):
         raise("html not in Content-Type")

    data = urlop.read().decode('utf-8')
    fsData.write(data)
    fsData.close()

    #解析html
    parser = etree.HTMLParser()
    tree= etree.parse(StringIO(data), parser)

    #print (etree.tostring(etree.HTML(data)))
    #print (tree.xpath("//img/@data-original"))
    #imghrefs=['http:'+img for img in tree.xpath("//img/@data-original") if img[0:4] != 'http' ]
    imghrefs=['http:'+img for img in tree.xpath("//img/@data-original") if img and img.strip() !="" and img[0:4] != 'http' ]
    #imghref=[img.attrib['src'] for img in tree.xpath("//img")]
    #print (imghrefs)
    #print (len(imghrefs))

    x=0
    for imgurl in imghrefs:
        print(imgurl)
        request.urlretrieve(imgurl, imgPath+'%s.jpg' %  x)
        x+=1


   # imghref=[img.attrib['data-original'] for img in tree.xpath("//img")]
   # print (imghref)

    print('==============Success==============')
except Exception as e:
    print(e)
    print('==============failed==============')


