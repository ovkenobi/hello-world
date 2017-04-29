from urllib import request
import re

def proxy_list(pages=1, loop = False):
    '''
    Функция генератор, возвращает список доступных прокси с сайта
    samair.ru. - устарел, новый https://premproxy.com/proxy/
    page - кол-во страниц (от 1 до примерно 50) для поиска.
    На 1 странице 35 прокси.
    '''
    def search_one(pattern, text):
        '''
        Функция поиска текста по шаблону
        Ищет только одно совпадение
        '''
        if pattern and text:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                i,j=match.span()
                return text[i:j]
        return None

    def search_all(pattern, text):
        '''
        Функция поиска текста по шаблону
        Ищет все совпадения, возвращает лист
        '''
        if pattern and text:
            return re.findall(pattern, text, re.DOTALL)
        return None
                

    def get_url(n=1):
        url = "https://premproxy.com/proxy"
        if n>1: url+= "/proxy-%02d.htm" % (n)
        return url
#        try: t = request.urlopen(url).readall().decode()
#        except:
#            t=None
#        t = search(r'id="navbuttons', t)
#        t = search("href=.+?>", t)
#        if t: t="https://premproxy.com"+t[6:-2]
#        return t

    while True:
        for i in range(pages):
            try: t = request.urlopen(get_url(i+1)).readall().decode()
            except: t = None
            t = search_one(r'<table[^>]+?id="proxylist.+?</table>', t)
            if t:
                for proxy in search_all(r"<tr.+?<td>.+?</td>", t):
                    proxy = search_one(r"<td>.+?</td>", proxy)
                    if proxy:
                        yield tuple(proxy[4:-5].strip().split(':'))
        if not loop: break

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

def gen_proxy_handler(proxies = proxy_list(20)):
    '''
    Генератор получающий на входе список прокси, которые нужно проверить.
    На выход выдает список ProxyHandler, с проверенным прокси
    '''
    for ip, port in proxies:
        if check_proxy2(ip, port):
            yield request.ProxyHandler({'http': 'http://{}:{}'.format(ip, port)})

class ProxyGenerator():
    def __init__(self):
        self.cur_proxy_handler=None
        self.proxy_gen=gen_proxy_handler(proxy_list(50, True))

    def next_handler(self):
        self.cur_proxy_handler = next(self.proxy_gen)
        return self.cur_proxy_handler
        
    def get_handler(self):
        if self.cur_proxy_handler is None: self.next_handler()
        return self.cur_proxy_handler


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
    for handler in gen_proxy_handler(proxy_list()):
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

def test_class_proxy_gen():
    print("--- testing ---")
    print("test class gen - 1")
    gen = ProxyGenerator()
    for _ in range(3):
        print(gen.get_handler().proxies['http'])
    print("test class gen - 2")
    for _ in range(3):
        print(gen.next_handler().proxies['http'])
    print("test class gen - 3")
    for _ in range(3):
        print(gen.next_handler().proxies['http'])
        print(gen.get_handler().proxies['http'])
    print("--- end -------")

def main():
    test_class_proxy_gen()
#    test_gen_proxy_handler()
#    test_proxy_list()
#    test_check_proxy_function(check_proxy)
#    test_check_proxy_function(check_proxy2)
#    test_check_proxy_function(check_proxy3)

if __name__ == "__main__":
    main()
