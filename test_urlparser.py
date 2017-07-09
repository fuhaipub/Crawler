from urllib.parse import urlparse

url_str = "http://www.163.com/mail/abc/adfa/index.htm"
url = urlparse(url_str)
print (url)
print ('protocol:%s'% url.scheme)
print ('hostname:%s'% url.hostname)
print ('port:%s'% url.port)
print ('path:%s'% url.path)

print (url.path.split('/')[-1])

i = len(url.path) - 1
while i > 0:
    if url.path[i] == '/':
        break
    i = i - 1
print ('filename:%s' % url.path[i+1:len(url.path)])