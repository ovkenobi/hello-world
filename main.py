import check_proxy
import proxy_list
from urllib import request

def next_proxy():
    for ip, port in proxy_list.proxy_list(1):
        print("check")
        if check_proxy.check_proxy2(ip, port):
            print(ip, port)
            yield (ip, port)

def main():
    ip, port = next(next_proxy())
    print("main", ip, port)
    proxy_handler = request.ProxyHandler({'http': 'http://{}:{}'.format(ip, port)})
    opener = request.build_opener(proxy_handler)
    try: r = opener.open("http://auto.e1.ru/car/foreign/?region[]=213", timeout=100)
    except: r = None
    if r:
        for key, value in dict(r.headers).items():
            print(key, value)
    

if __name__ == "__main__":
    print("begin")
    #main()
    print('end')
