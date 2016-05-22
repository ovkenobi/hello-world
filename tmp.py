from urllib import request
from datetime import datetime
from json import dumps
from json import loads

def load_page(iter_links, iter_proxy, need_head=False):
    print('begin load_page')
    last_ok = True
    while True:
        print("select proxy")
        proxy_handler = next(iter_proxy)
        print("proxy selected", proxy_handler.proxies['http'])
        opener = request.build_opener(proxy_handler)
        opener.addheaders.clear()
        while True:
            if last_ok: link = next(iter_links)
            print('link', link)
            last_ok = False
            text = None
            try:
                r = opener.open(link, timeout=30)
                text = r.readall().decode()
            except: 
                print("error")
                break
            if not text: break
            print('load link ok')
            last_ok = True
            if need_head: yield text, dict(r.headers)
            else: yield text

#asdas            
def request_post(url, proxy, body=None, headers=None):
    opener = request.build_opener(proxy)
    opener.addheaders = headers
    try:
        r = opener.open(url, data=body, timeout=30)
    except Exception as e:
        print('Error =', e)
        r = None
    if r:
#        print(dict(r.headers))
        t=r.readall()
        print(t)
        t=t.decode()
        t=loads(t)
        print(t)
        return t
    print('None')
    return None
        
if __name__ == "__main__":
    print()
    print()
    print()
    print()
    print()
    proxy_handler=request.ProxyHandler({'http':'http://89.235.174.160:8080'})
    url = "http://auto.e1.ru/offer/json"
    data = dumps({"jsonrpc":"2.0",
              "method":"getOfferContacts",
              "params":[{"id":"7356291",
                         "context":"card"}],
              "id":int(datetime.now().timestamp()*1000)})

    data=data.encode()
    
    headers = [
    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
    ('Content-Length', len(data)),
    ('Referer', url),
    ('Cookie', 'ngs_ttq=u:7ab7b9cd7017c3a1b331f8030bf1bf55;\
                ngs_uid=w127Clcq97gyuAyVA8NYAg==; \
                isMobile=false; \
                _ym_uid=1462433727342287192; \
                _ym_visorc_24038521=w; \
                _ym_isad=2; \
                __utma=8453157.762694507.1462433727.1462433727.1462433727.1; \
                __utmb=8453157.6.10.1462433727; \
                __utmc=8453157; \
                __utmz=8453157.1462433727.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); \
                ngs_avc=9; \
                RT=; \
                doh=10; \
                presentationListHide=true; \
                __utmt=1')
    ]
    request_post(url, proxy_handler, body=data, headers=headers)





