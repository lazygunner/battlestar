# encoding: UTF-8
import re

def getDownloadLink(url):
    p = re.compile(r'&amp;')
    url = p.sub('&', url, 1)
    match = re.search(r'http:\/\/(?:pan|yun).baidu.com\/share\/link\?shareid=(\d+)&uk=(\d+)',url)
    if(match):
        import urllib,urllib2
        id = match.group(1)
        uk = match.group(2)
        header = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14'
        }
        request = urllib2.Request(url = url, headers = header)
        html_code = urllib2.urlopen(request).read()

        #"md5\":\"88296788f23f16396e05e75a037bac00\"
        md5_match = re.search(r'"md5\\":\\\"(.+?)\\"',html_code)

        if(md5_match):
            md5 = md5_match.group(1)
            #dlink\\":.+?(http.+?88296788f23f16396e05e75a037bac00\?.+?sh=1)
            reg = 'dlink\\\\":.+?(http.+?' + md5 + '\?.+?sh=1)'
            print reg;
            match = re.search(reg,html_code,re.MULTILINE)
            if(match):
                return {
                        'url': url,
                        'error':False,
                        'link':match.group(1).replace("\\","")
	                    }			
            else:
                return {} 
#		else:
#            return 
#	else:
#        return 

