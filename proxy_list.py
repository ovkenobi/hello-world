from urllib import request
import re

def proxy_list(pages=1):
    def search(pattern, text):
        if pattern and text:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                i,j=match.span()
                return text[i:j]
        return None

    def get_url(n=1):
        if n==1: url = "http://samair.ru/proxy"
        else: url = "http://samair.ru/proxy/proxy-%02d.htm" % (n)
        try: t = request.urlopen(url).readall().decode()
        except: t=None
        t = search(r"Can\'t copy proxy ports\?.*?You can do it there", t)
        t = search("href=.+?>", t)
        if t: t="http://samair.ru"+t[6:-2]
        return t
    
    res = set()
    for i in range(pages):
        try: t = request.urlopen(get_url(i+1)).readall().decode()
        except: t = None
        t = search(r'id="content.+?</div>', t)
        t = search(r"<pre>.+?</pre>", t)
        if t:
            for proxy in t[5:-6].strip().split('\n'):
                res.add(tuple(proxy.split(':')))
    return res


def start_test():
    for ip, port in proxy_list(1):
       print(ip,':',port, sep='')

        
if __name__=="__main__":
    start_test()
