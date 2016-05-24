import tmp
from json import dumps
from datetime import datetime
from proxies import gen_proxy_handler
from auto_e1_parse2 import all_href_car
from auto_e1_parse2 import get_public_info
from auto_e1_parse2 import get_private_info
from string import printable
from random import sample
from random import randrange


def get_random_str(length):
    return ''.join(sample(printable[:62],length))

def gen_url(n):
    yield "http://auto.e1.ru/car/foreign/?region[]=213"
    for i in range(n-1):
        yield "http://auto.e1.ru/car/foreign/?region[]=213&page={}".format(i+2)

def make_json_body(id_):
    return dumps({"jsonrpc":"2.0",
                  "method":"getOfferContacts",
                  "params":[{"id": id_,
                  "context":"card"}],
                  "id":int(datetime.now().timestamp()*1000)}).encode()

def make_headers(length, cookie_part):
    return list({'Accept': 'application/json, text/javascript, */*; q=0.01',
                 'Content-Length': length,
                 'Referer': "http://auto.e1.ru/offer/json",
                 'Cookie': cookie_part+"; ngs_ttq={}; ngs_uid={}; ngs_avc={};".format(get_random_str(34),get_random_str(24),randrange(7,40))
                 }.items())


def main2():
    url = "http://auto.e1.ru/offer/json"
#    headers = {
#        'Accept': 'application/json, text/javascript, */*; q=0.01',
#        'Content-Length': 0,
#        'Referer': url,
#        'Cookie': ""
#        }

    file = open("data.txt", 'w')
    count = 0
    handlers = gen_proxy_handler()
    for page_lavel_1 in tmp.load_page(gen_url(10), handlers):
        for page_lavel_2, head in tmp.load_page(all_href_car(page_lavel_1), handlers, True):
            count +=1
#            cookies=head['Set-Cookie']+"; ngs_ttq={}; ngs_uid={}; ngs_avc={};".format(get_random_str(34),get_random_str(24),count%30+7)
#            print(count, cookies)
            d=get_public_info(page_lavel_2)
            data = make_json_body(d['id'])
            handler = next(handlers)
            for _ in range(3):
                r = tmp.request_post(url, handler, data, make_headers(len(data), head['Set-Cookie']))
                if r:
                    d1=get_private_info(r)
                    if d1: d.update(d1)
                    break
            print(count, d['title'], d.get('phone', ''))
#            file.write(dumps(d))
#            file.write('\n')
#            file.flush()
    file.close()


class ParserE1():
    def __init__(self):
        self.url = "http://auto.e1.ru/offer/json"
        self.cur_proxy_handler=None
        self.gen_proxy_handler=None
        self.last_headers = None
        self.last_cookies = None
        
    def next_proxy_handler(self):
        if self.gen_proxy_handler is None: raise Exception("Generator for proxy handlers is 'None'")
        self.cur_proxy_handler = next(self.gen_proxy_handler)

    def make_headers(self, length):
        if self.last_cookies is None: raise Exception("Can't make 'Headers' because cookies is 'None'")
        return list({'Accept': 'application/json, text/javascript, */*; q=0.01',
                     'Content-Length': length,
                     'Referer': "http://auto.e1.ru/offer/json",
                     'Cookie': "ngs_ttq={}; ngs_uid={}; ngs_avc={}; ".format(get_random_str(34),get_random_str(24),randrange(7,40))+self.last_cookies
                     }.items())

    def gen_url(self, n):
        yield "http://auto.e1.ru/car/foreign/?region[]=213"
        for i in range(n-1):
            yield "http://auto.e1.ru/car/foreign/?region[]=213&page={}".format(i+2)

    def set_headers(self, headers):
        self.last_headers = headers
        if "Set-Cookie" in headers:
            self.last_cookies = headers["Set-Cookie"]

    def load_page(self, iter_links):
        if self.cur_proxy_handler is None: self.next_proxy_handler()
        print('load_page - start')
        last_ok = True
        while True:
            print("proxy selected", self.cur_proxy_handler.proxies['http'])
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
                    if err_num > 3:
                        self.next_proxy_handler()
                        break
                    continue
                print('load link - ok')
                last_ok = True
                self.set_headers(dict(r.headers))
                yield text

    def request_post(self, url, body=None):
        for _ in range(3):
            opener = request.build_opener(self.cur_proxy_handler)
            for __ in range(3):
                opener.addheaders = self.make_headers(len(body))
                
                
        print("request_post start")
        t = None
        try:
            r = opener.open(url, data=body, timeout=30)
            t = r.readall().decode()
        except http.client.HTTPException as e: print("HTTPException =", e)
        except error.HTTPError as e: print('HTTPError =', e)
        except error.URLError as e: print('URLError =', e)
        except Exception as e: print("Exception =", e)
        if t:
            print("request_post Ok")
            #print(t)
            return loads(t)['result']
        print('None')
        return None



if __name__ == "__main__":
    print("begin")
    main2()
    print('end')
