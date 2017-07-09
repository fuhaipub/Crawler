# -*- coding: utf-8 -*-
import re
import urllib.request
import urllib
import http.cookiejar
from io import StringIO, BytesIO
from lxml import etree
from urllib import request
import zlib
import json
import findScriptParams
import codecs



'''
'http://www.yy.com/more/page.action?biz=sing&subBiz=idx&moduleId=679 ',


        	var totalPages = 42;
        	var totalCount = 1003;
        	var moduleId = '328';
        	var biz = 'talk';
        	var subBiz = 'idx';
			var showImpress = true;


GET http://www.yy.com/more/page.action?biz=sing&subBiz=pop&page=20&moduleId=476 HTTP/1.1
X-Requested-With: XMLHttpRequest
Accept: application/json, text/javascript, */*; q=0.01
Referer: http://www.yy.com/music/pop/more/476
Accept-Language: zh-CN
Accept-Encoding: gzip, deflate
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko
Connection: Keep-Alive
Host: www.yy.com
Cookie: hiido_ui=0.5000765156789647; hd_newui=0.707248601400319; Hm_lvt_c493393610cdccbddc1f124d567e36ab=1498149737; Hm_lpvt_c493393610cdccbddc1f124d567e36ab=1498149780; hdjs_session_id=0.13294339780717884; hdjs_session_time=1498149779972
'''

# head: dict of header
def makeMyOpener(head = {
    'X-Requested-With':'XMLHttpRequest',
    'Connection': 'Keep-Alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Host': 'www.yy.com',
    'Referer': 'http://www.yy.com/music/pop/more/476'
}):
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener


def downloadMoreImg(html_data, imgPath='C:\\pyProject\\Crawler\\img\\'):

    oper = makeMyOpener()

    try:
        totalPages = re.compile(r'var totalPages = (.+?);').findall(html_data)[0]
        totalCount = re.compile(r'var totalCount = (.+?);').findall(html_data)[0]
        moduleId = re.compile('var moduleId = \'(.+?)\';').findall(html_data)[0]
        biz = re.compile(r'var biz = \'(.+?)\';').findall(html_data)[0]
        subBiz = re.compile(r'var subBiz = \'(.+?)\';').findall(html_data)[0]

        totalPages = int(totalPages)
        totalCount = int(totalCount)

        if not (totalPages and totalCount and moduleId and biz and subBiz):
            return

        for page in range(1,totalPages):
            url = 'http://www.yy.com/more/page.action?biz=%s&subBiz=%s&moduleId=%s&page=%d' %(biz,subBiz,moduleId,page )
            print ("通过XmlHTTPRequest获取图片__%s" % url)

            urlop = oper.open(url, timeout=3)
            jsondata = zlib.decompress(urlop.read(), 16+zlib.MAX_WBITS)
            hjson = json.loads(jsondata.decode('utf-8'))

            count=0
            for dd in hjson['data']['data']:
                request.urlretrieve(dd['thumb'], imgPath+'%s_%s_%s_%d_%d.jpg' % (biz,subBiz,moduleId,page,count ))
                count +=1
                #if dd['thumb'] != dd['thumb2']:
                #    request.urlretrieve(dd['thumb2'], imgPath+'%s_%s_%s_%d_%d.jpg' % (biz,subBiz,moduleId,page,count ))
                #    count +=1
            print ("通过XmlHTTPRequest获取第%d页,%s_%s_%s,共%d张图片" % (page,biz,subBiz,moduleId,count))

    except Exception as e:
        #print (e)
        pass




if __name__ == "__main__":
    def makeMyOpener2(head = {
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


    opener = makeMyOpener2()
    urlop = opener.open("http://www.yy.com/music/dance/more/678", timeout=3)
    data =  urlop.read().decode('utf-8')
    if 'html' not in urlop.getheader('Content-Type'):
        exit
    #print (data)
    downloadMoreImg(data)
