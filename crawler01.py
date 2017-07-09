import re
import urllib.request
import urllib
import http.cookiejar

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
urlDataFile="urldata.txt"

fsLog=open(logfilename,'w')
fsData=open(urlDataFile,'w',encoding='utf-8')

queue = deque()
visited = set()

#url = 'http://www.hao123.com'  # 入口页面, 可以换成别的
#url = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%BE%8E%E5%A5%B3&oq=%E7%BE%8E%E5%A5%B3&rsp=-1'
url ='http://www.yy.com/music/'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()  # 队首元素出队 visited |= {url}  # 标记为已访问

    log= 'Get URL: ' + str(cnt) + ' Getting<---  ' + url
    fsLog.write(log+'\n')
    print (log)
    cnt += 1

    oper = makeMyOpener()
    try:
        urlop = oper.open(url, timeout=3)
        #urlop = urllib.request.urlopen(url,timeout=2)
        if 'html' not in urlop.getheader('Content-Type'):
            continue
        data = urlop.read().decode('utf-8')
        #data = urlop.read().decode('gbk')
        fsData.write(data)
    except Exception as e:
        print(e)
        continue

    # 正则表达式提取页面中所有队列, 并判断是否已经访问过, 然后加入待爬队列
    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            log='Add URL Queue--->  ' + x +'Queue length' +str(len(queue))
            fsLog.write(log+'\n')
            print (log)