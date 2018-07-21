 # -*- coding: utf-8 -*-
import re
import codecs


#    'http://www.yy.com/more/page.action?biz=sing&subBiz=idx&moduleId=679 ',
'''
        	var totalPages = 42;
        	var totalCount = 1003;
        	var moduleId = '328';
        	var biz = 'talk';
        	var subBiz = 'idx';
			var showImpress = true;

fs = open('C:\\pyProject\\Crawler\\urldata.txt','r',encoding='utf-8')

html= fs.read()
print(type(html))
'''
def getMoreImgUrl(html):
    try:
        totalPages = re.compile(r'var totalPages = (.+?);').findall(html)[0]
        totalCount = re.compile(r'var totalCount = (.+?);').findall(html)[0]
        moduleId = re.compile('var moduleId = \'(.+?)\';').findall(html)[0]
        biz = re.compile(r'var biz = \'(.+?)\';').findall(html)[0]
        subBiz = re.compile(r'var subBiz = \'(.+?)\';').findall(html)[0]

        url = "http://www.yy.com/more/page.action?biz=%s&subBiz=%s&moduleId=%s" % (biz,subBiz,moduleId)
        return {'totalPages':totalPages,'url':url}

    except Exception as e:
        if debug :print(e)
        return None



