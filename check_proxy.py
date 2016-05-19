from urllib import request
import re

def check_proxy(ip,port):
    url = 'http://api.proxyipchecker.com/pchk.php'
    data = "ip={}&port={}".format(ip, port).encode()
    req = request.Request(url, data=data, method='POST')
    try: t = request.urlopen(req).readall().decode()
    except: return False
    try:
        #if float(t.split(';')[0])<6: return True
        print(t.split(';'))
        return True
    except: pass
    return False

def check_proxy2(ip, port):
    url = 'http://ip-detect.ru/'
    proxy_handler = request.ProxyHandler({'http': 'http://{}:{}'.format(ip,port)})
    opener = request.build_opener(proxy_handler)
    try: t = opener.open(url, timeout=5).readall().decode()
    except: t = None
    if t:
        match = re.search(r'<div.+?my_ip".*?>.+?</div>', t)
        if match:
            i,j = match.span()
            if ip in t[i:j]: return True
    return False

def check_proxy3(ip, port):
    proxy_handler = request.ProxyHandler({'http': 'http://{}:{}'.format(ip,port)})
    opener = request.build_opener(proxy_handler)
    
    my_ip=["http://ipinfo.io/ip",
           "https://icanhazip.com",
           "http://checkip.dyndns.org",
           "https://api.ipify.org"]
    
    for site in my_ip:
        try: t=opener.open(site, timeout=5).readall().decode()
        except: return False
        if ip not in t: return False
        return True

def start_tests():
    l = ["31.168.236.236:8080",
         "185.135.68.30:80",
         "138.185.238.66:9000",
         "210.96.153.20:3128",
         "177.223.63.30:8080",
         "64.53.217.196:8080",
         "203.201.37.77:80",
         "134.196.214.127:3128",
         "119.93.82.148:80",
         "81.218.197.25:8088",
         "78.40.181.45:80",
         "190.63.140.71:80",
         "89.235.174.160:8080",
         "122.121.221.236:3128",
         "182.253.191.131:8080"
        ]
    for ip, port in map(lambda x:x.split(':'), l):
        print(ip, check_proxy(ip, port))


if __name__ == "__main__":
    start_tests()

