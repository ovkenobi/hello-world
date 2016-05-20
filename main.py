import tmp
import json
from proxies import gen_proxy_handler
from auto_e1_parse2 import all_href_car
from auto_e1_parse2 import get_public_info

def gen_url(n):
    yield "http://auto.e1.ru/car/foreign/?region[]=213"
    for i in range(n-1):
        yield "http://auto.e1.ru/car/foreign/?region[]=213&page={}".format(i+2)


def main2():
    file = open("data.txt", 'w')
    count = 0
    handlers = gen_proxy_handler()
    for page_lavel_1 in tmp.load_page(gen_url(10), handlers):
        for page_lavel_2 in tmp.load_page(all_href_car(page_lavel_1), handlers):
            count +=1
            d=get_public_info(page_lavel_2)
            print(count, d['title'])
            file.write(json.dumps(d))
            file.write('\n')
            file.flush()
    file.close()


if __name__ == "__main__":
    print("begin")
    main2()
    print('end')
