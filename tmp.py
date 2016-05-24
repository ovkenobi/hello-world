from urllib import request
from urllib import error
from json import dumps
from json import loads
import http

def load_page(iter_links, iter_proxy, need_head=False):
    print('load_page - start')
    last_ok = True
    while True:
        print("select proxy")
        proxy_handler = next(iter_proxy)
        print("proxy selected", proxy_handler.proxies['http'])
        opener = request.build_opener(proxy_handler)
        opener.addheaders.clear()
        err_num=0
        while True:
            if last_ok: link = next(iter_links)
            print('link', link)
            last_ok = False
            text = None
            try:
                r = opener.open(link, timeout=30)
                text = r.readall().decode()
            except http.client.HTTPException as e: print("HTTPException =", e)
            except error.HTTPError as e: print('HTTPError =', e)
            except error.URLError as e: print("URLError =", e)
            if text is None:
                err_num +=1
                if err_num > 3: break
                continue
            print('load link - ok')
            last_ok = True
            if need_head: yield text, dict(r.headers)
            else: yield text

def request_post(url, proxy, body=None, headers=None):
    opener = request.build_opener(proxy)
    opener.addheaders = headers
    print("request_post start")
    t = None
    try:
        r = opener.open(url, data=body, timeout=30)
        t = r.readall()
    except http.client.HTTPException as e: print("HTTPException =", e)
    except error.HTTPError as e: print('HTTPError =', e)
    except error.URLError as e: print('URLError =', e)
    except Exception as e: print("Exception =", e)
    if t:
        print("request_post Ok")
        t=t.decode()
        #print(t)
        return loads(t)['result']
    print('None')
    return None

def test_request_post():
    from auto_e1_parse2 import get_private_info
    proxy_handler=request.ProxyHandler({'http':'http://210.96.153.20:3128'})
    url = "http://auto.e1.ru/offer/json"
    data = dumps({"jsonrpc":"2.0",
              "method":"getOfferContacts",
              "params":[{"id":"7684741",
                         "context":"card"}],
              "id":1463980588546})
    data=data.encode()
    headers = [
    ('Accept', 'application/json, text/javascript, */*; q=0.01'),
    ('Content-Length', len(data)),
    ('Referer', url),
    ('Cookie', 'ngs_ttq=u:7ab7b9cd7017c3a1b331a8030bf1bf;\
                ngs_uid=w127Clcq97GyuAyVA8NYAg; \
                isMobile=false; \
                ngs_avc=39; \
                ')
    ]
    res= request_post(url, proxy_handler, body=data, headers=headers)
    print("type res = ", type(res))
    print(get_private_info(res))

def test_load_page():
    url_list = ["http://auto.e1.ru/car/foreign/?region[]=213",
                "http://auto.e1.ru/car/foreign/?region[]=213&page=2",
                "http://auto.e1.ru/car/foreign/?region[]=213&page=3"]
    proxy_list = [request.ProxyHandler({'http':'http://203.201.37.77:80'}),
                  request.ProxyHandler({'http':'http://177.223.63.30:8080'}),
                  request.ProxyHandler({'http':'http://210.96.153.20:3128'}),
                  request.ProxyHandler({'http':'http://81.218.197.25:8088'})]
    for text in load_page(iter(url_list), iter(proxy_list)):
        print(text)

if __name__ == '__main__':
    #test_load_page()
    test_request_post()
