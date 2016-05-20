from urllib import request
import re

def proxy_list(pages=1):
    '''
    Функция генератор, возвращает список доступных прокси с сайта samair.ru.
    page - кол-во страниц (от 1 до примерно 50) для поиска.
    На 1 странице 35 прокси.
    '''
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
    
    for i in range(pages):
        try: t = request.urlopen(get_url(i+1)).readall().decode()
        except: t = None
        t = search(r'id="content.+?</div>', t)
        t = search(r"<pre>.+?</pre>", t)
        if t:
            for proxy in t[5:-6].strip().split('\n'):
                yield tuple(proxy.split(':'))

def check_proxy(ip,port):
    '''
    Проверяет доступность прокси с помощью API сайта proxyipchecker.com.
    Часто результат положительный    
    '''
    url = 'http://api.proxyipchecker.com/pchk.php'
    data = "ip={}&port={}".format(ip, port).encode()
    req = request.Request(url, data=data, method='POST')
    try: t = request.urlopen(req).readall().decode()
    except: return False
    try:
        if float(t.split(';')[0])<6: return True
    except: pass
    return False

def check_proxy2(ip, port):
    '''
    Проверяет прокси на скрытие ip. Делает запрос на сайт ip-detect.ru, и
    парсит ответ. Прокси сервер считается проверенным, если в полученном ответе
    его IP-адрес.
    '''
    url = 'http://ip-detect.ru/'
    proxy_handler = request.ProxyHandler({'http': 'http://{}:{}'.format(ip,port)})
    opener = request.build_opener(proxy_handler)
    try: t = opener.open(url, timeout=3).readall().decode()
    except: t = None
    if t:
        match = re.search(r'<div.+?my_ip".*?>.+?</div>', t)
        if match:
            i,j = match.span()
            if ip in t[i:j]: return True
    return False

def check_proxy3(ip, port):
    '''
    Аналогично check_proxy2. За тем исключением, что здесь посылается несколько
    запросов, разным сайтам. Общее у сайтов то, что они предоставляют удобный API
    '''
    my_ip=("http://ipinfo.io/ip",
           "https://icanhazip.com",
           "http://checkip.dyndns.org",
           "https://api.ipify.org")
    proxy_handler = request.ProxyHandler({'http': 'http://{}:{}'.format(ip,port)})
    opener = request.build_opener(proxy_handler)
    for site in my_ip:
        try: t=opener.open(site, timeout=3).readall().decode()
        except: return False
        if ip not in t: return False
        return True

def gen_proxy_handler(proxies = proxy_list(50)):
    '''
    Генератор получающий на входе список прокси, которые нужно проверить.
    На выход выдает список ProxyHandler, с проверенным прокси
    '''
    for ip, port in proxies:
        if check_proxy2(ip, port):
            yield request.ProxyHandler({'http': 'http://{}:{}'.format(ip, port)})

__proxies = (
    ("31.168.236.236",8080),
    ("185.135.68.30",80),
    ("138.185.238.66",9000),
    ("210.96.153.20",3128),
    ("177.223.63.30",8080),
    ("64.53.217.196",8080),
    ("203.201.37.77",80),
    ("134.196.214.127",3128),
    ("119.93.82.148",80),
    ("81.218.197.25",8088),
    ("78.40.181.45",80),
    ("190.63.140.71",80),
    ("89.235.174.160",8080),
    ("122.121.221.236",3128),
    ("182.253.191.131",8080)
    )

def test_gen_proxy_handler():
    print("--- testing ---")
    print("test proxy gen 1")
    for handler in gen_proxy_handler(__proxies):
        print(handler.proxies['http'])
    print()
    print("test proxy gen 2")
    for handler in gen_proxy_handler():
        print(handler.proxies['http'])
    print()
    print("--- end -------")

def test_check_proxy_function(fun_check):
    print("--- testing ---")
    print("test",fun_check.__name__)
    for ip,port in __proxies:
        print(ip,':',port,' - ',fun_check(ip,port),sep='')
    print("--- end -------")

def test_proxy_list():
    print("--- testing ---")
    print("test proxy_list - 1")
    for ip,port in proxy_list():
        print(ip,':',port,sep='')
    print()
    print("test proxy_list - 2")
    for ip,port in proxy_list(2):
        print(ip,':',port,sep='')
    print()
    print("test proxy_list - 3")
    for ip,port in proxy_list(3):
        print(ip,':',port,sep='')
    print()
    print("--- end -------")

def main():
    test_gen_proxy_handler();
#    test_proxy_list()
#    test_check_proxy_function(check_proxy)
#    test_check_proxy_function(check_proxy2)
#    test_check_proxy_function(check_proxy3)

if __name__ == "__main__":
    main()
