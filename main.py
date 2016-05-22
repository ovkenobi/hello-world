import tmp
from json import dumps
from datetime import datetime
from proxies import gen_proxy_handler
from auto_e1_parse2 import all_href_car
from auto_e1_parse2 import get_public_info
from auto_e1_parse2 import get_private_info

def gen_url(n):
    yield "http://auto.e1.ru/car/foreign/?region[]=213"
    for i in range(n-1):
        yield "http://auto.e1.ru/car/foreign/?region[]=213&page={}".format(i+2)


def main2():
    url = "http://auto.e1.ru/offer/json"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Length': 0,
        'Referer': url,
        'Cookie': ""
        }

    file = open("data.txt", 'w')
    count = 0
    handlers = gen_proxy_handler()
    for page_lavel_1 in tmp.load_page(gen_url(10), handlers):
        for page_lavel_2, head in tmp.load_page(all_href_car(page_lavel_1), handlers, True):
            count +=1
            d=get_public_info(page_lavel_2)
            
            data = dumps({"jsonrpc":"2.0",
                          "method":"getOfferContacts",
                          "params":[{"id":d['id'],
                          "context":"card"}],
                          "id":int(datetime.now().timestamp()*1000)}).encode()
            headers['Content-Length'] = len(data)
            headers['Cookie'] = head['Set-Cookie']
            r=tmp.request_post(url, next(handlers), data, list(headers.items()))
            if r:
                d1=get_private_info(tmp.request_post())
                if d1: d.update(d1)
            print(count, d['title'])
            file.write(json.dumps(d))
            file.write('\n')
            file.flush()
    file.close()


if __name__ == "__main__":
    print("begin")
    main2()
    print('end')
