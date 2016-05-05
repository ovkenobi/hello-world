import requests
import re
from datetime import datetime
from json import dumps
'''
https://gist.github.com/jefftriplett/9748036
https://www.ipify.org/
https://stackoverflow.com/questions/10967631/how-to-make-http-request-through-a-tor-socks-proxy-using-python
'''


headerPost = {'Host': 'auto.e1.ru',
              'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0',
              'Accept': 'application/json, text/javascript, */*; q=0.01',
              'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
              'Accept-Encoding': 'gzip, deflate',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'X-Requested-With': 'XMLHttpRequest',
              'Referer': 'http://auto.e1.ru/car/used/opel/opel_astra/7511983',
              'Content-Length': '107',
              'Cookie': 'ngs_ttq=u:7ab7b9cd7017c3a1b331f8030bf1bf55; ngs_uid=w127Clcq97gyuAyVA8NYAg==; isMobile=false; _ym_uid=1462433727342287192; _ym_isad=2; __utma=8453157.762694507.1462433727.1462437657.1462441152.3; __utmc=8453157; __utmz=8453157.1462433727.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ngs_avc=3; doh=10; region_location=%5B213%5D; location=%7B%22type%22%3A%22region%22%2C%22value%22%3A%5B213%5D%7D; search_offers_persistent=a%3A3%3A%7Bs%3A8%3A%22currency%22%3Bs%3A3%3A%22rur%22%3Bs%3A5%3A%22limit%22%3Bi%3A20%3Bs%3A4%3A%22sort%22%3Ba%3A16%3A%7Bs%3A2%3A%22id%22%3BN%3Bs%3A4%3A%22date%22%3BN%3Bs%3A14%3A%22date_and_price%22%3BN%3Bs%3A10%3A%22mark_model%22%3BN%3Bs%3A4%3A%22year%22%3BN%3Bs%3A10%3A%22horsepower%22%3BN%3Bs%3A12%3A%22transmission%22%3BN%3Bs%3A6%3A%22engine%22%3BN%3Bs%3A8%3A%22capacity%22%3BN%3Bs%3A11%3A%22engine_type%22%3BN%3Bs%3A5%3A%22wheel%22%3BN%3Bs%3A4%3A%22city%22%3BN%3Bs%3A8%3A%22run_size%22%3BN%3Bs%3A4%3A%22gear%22%3BN%3Bs%3A5%3A%22price%22%3BN%3Bs%3A11%3A%22views_total%22%3BN%3B%7D%7D; search_offers=a%3A0%3A%7B%7D; search_window=table; presentationListHide=true; _ym_visorc_24038521=w; __utmb=8453157.1.10.1462441152; __utmt=1; RT=',
              'Connection': 'keep-alive'}

exampleJsonRequests={"jsonrpc":"2.0","method":"getOfferContacts","params":[{"id":7844147,"context":"card"}],"id":1462441745973}

# {"jsonrpc":"2.0","result":"<div class=\"au-offer-card__contacts _offer_contacts   au-offer-card__contacts_opened\"  data-offer_id=\"7844147\" data-context=\"card\"><div class=\"au-offer-card__contacts-inner _contacts\"><div class=\"au-offer-card__contacts-box\"><h3 class=\"au-offer-card__contacts-title\">\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u0430<\/h3><div class=\"au-offer-card__contacts-block au-offer-card__contacts-block_box\"><span class=\"au-offer-card__contacts-phone\"><span class=\"au-offer-card__contacts-phone-txt\">+7-912-628-52-00<\/span><\/span><\/div><div class=\"au-offer-card__contacts-block au-offer-card__contacts-block_question\"><a href=\"\" class=\"au-offer-card__contacts-link au-offer-card__contacts-link_dotted _question_link\" data-tab=\"_questions\"><span class=\"au-offer-card__contacts-txt\">\u0417\u0430\u0434\u0430\u0442\u044c \u0432\u043e\u043f\u0440\u043e\u0441 \u043f\u0440\u043e\u0434\u0430\u0432\u0446\u0443<\/span><\/a><\/div><div class=\"au-offer-card__contacts-block au-offer-card__contacts-block_mail au-offer-card__contacts-mail\"><a class=\"au-offer-card__contacts-link au-offer-card__contacts-link_dotted _send_seller_mail\" href=\"javascript:void(null);\" data-offer_id=\"7844147\"><span class=\"au-offer-card__contacts-txt\">\u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u043f\u0438\u0441\u044c\u043c\u043e<\/span><\/a><\/div><div class=\"au-offer-card__contacts-block\"><a href=\"\" class=\"au-offer-card__contacts-link au-offer-card__contacts-link_dotted _offer_sold_link\"><span class=\"au-offer-card__contacts-txt\">\u0421\u043e\u043e\u0431\u0449\u0438\u0442\u044c, \u0447\u0442\u043e \u0430\u0432\u0442\u043e \u043f\u0440\u043e\u0434\u0430\u043d\u043e<\/span><\/a><span class=\"au-offer-card__contacts-txt au-offer-card__contacts-txt_sold _sold_msg hidden\">\u041e\u0431\u044a\u044f\u0432\u043b\u0435\u043d\u0438\u0435 \u0431\u0443\u0434\u0435\u0442 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e<\/span><div class=\"_offer_sold_title hidden\">\u0412\u044b \u043f\u043e\u0437\u0432\u043e\u043d\u0438\u043b\u0438 \u0438 \u043f\u0440\u043e\u0434\u0430\u0432\u0435\u0446 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u043b, \u0447\u0442\u043e \u0430\u0432\u0442\u043e \u043f\u0440\u043e\u0434\u0430\u043d\u043e?<\/div><div class=\"_offer_sold_content hidden\"><button class=\"au-flat-button au-offer-card__contacts-button _sold_btn_approve\" data-id=\"7844147\">\u0414\u0430<\/button><button class=\"au-flat-button au-offer-card__contacts-button _sold_btn_reset\">\u041d\u0435\u0442<\/button><\/div><\/div><\/div><div class=\"au-offer-card__contacts-box\">\n\n                                                                                <\/div>\n            <\/div>\n            <\/div>\n\n\n            <div class=\"au-offer-card__velum\"><ul class=\"au-offer-card__velums-list\"><li class=\"au-offer-card__velums-item velum\"><\/li><li class=\"au-offer-card__velums-item velum\"><\/li><\/ul><\/div>\n    ","id":1462441745973}

def e1_auto_phone_number(car_id):
    header={'Host':'auto.e1.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'ngs_ttq=u:7ab7b9cd7017c3a1b331f8030bf1bf55; ngs_uid=w127Clcq97gyuAyVA8NYAg==; isMobile=false; _ym_uid=1462433727342287192; _ym_visorc_24038521=w; _ym_isad=2; __utma=8453157.762694507.1462433727.1462433727.1462433727.1; __utmb=8453157.6.10.1462433727; __utmc=8453157; __utmz=8453157.1462433727.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ngs_avc=9; RT=; doh=10; region_location=%5B213%5D; location=%7B%22type%22%3A%22region%22%2C%22value%22%3A%5B213%5D%7D; search_offers_persistent=a%3A3%3A%7Bs%3A8%3A%22currency%22%3Bs%3A3%3A%22rur%22%3Bs%3A5%3A%22limit%22%3Bi%3A20%3Bs%3A4%3A%22sort%22%3Ba%3A16%3A%7Bs%3A2%3A%22id%22%3BN%3Bs%3A4%3A%22date%22%3BN%3Bs%3A14%3A%22date_and_price%22%3BN%3Bs%3A10%3A%22mark_model%22%3BN%3Bs%3A4%3A%22year%22%3BN%3Bs%3A10%3A%22horsepower%22%3BN%3Bs%3A12%3A%22transmission%22%3BN%3Bs%3A6%3A%22engine%22%3BN%3Bs%3A8%3A%22capacity%22%3BN%3Bs%3A11%3A%22engine_type%22%3BN%3Bs%3A5%3A%22wheel%22%3BN%3Bs%3A4%3A%22city%22%3BN%3Bs%3A8%3A%22run_size%22%3BN%3Bs%3A4%3A%22gear%22%3BN%3Bs%3A5%3A%22price%22%3BN%3Bs%3A11%3A%22views_total%22%3BN%3B%7D%7D; search_offers=a%3A0%3A%7B%7D; search_window=table; presentationListHide=true; __utmt=1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'}
            
    url = "http://auto.e1.ru/offer/json"
    data = dumps({"jsonrpc":"2.0",
                  "method":"getOfferContacts",
                  "params":[{"id":car_id,
                             "context":"card"}],
                  "id":int(datetime.now().timestamp()*1000)})
        
    post_header = header
    post_header['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    post_header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
    post_header['X-Requested-With'] = 'XMLHttpRequest'
    post_header['Referer'] = url
    post_header['Content-Length'] = len(data)
    post_header.pop('Cache-Control')
    
    r=requests.post(url, data=data, headers=post_header)
    if r.status_code != 200: return None
    answer=r.json()
    if 'error' in answer: return None
    match = re.search("au-offer-card__contacts-phone-txt.+?<", answer['result'])
    if match:
        i,j=match.span()
        phone=answer['result'][i:j-1]
        return phone[phone.rfind(">")+1:]
    return None


def e1_auto_info(url):
    header={'Host':'auto.e1.ru',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:46.0) Gecko/20100101 Firefox/46.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Cookie': 'ngs_ttq=u:7ab7b9cd7017c3a1b331f8030bf1bf55; ngs_uid=w127Clcq97gyuAyVA8NYAg==; isMobile=false; _ym_uid=1462433727342287192; _ym_visorc_24038521=w; _ym_isad=2; __utma=8453157.762694507.1462433727.1462433727.1462433727.1; __utmb=8453157.6.10.1462433727; __utmc=8453157; __utmz=8453157.1462433727.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ngs_avc=9; RT=; doh=10; region_location=%5B213%5D; location=%7B%22type%22%3A%22region%22%2C%22value%22%3A%5B213%5D%7D; search_offers_persistent=a%3A3%3A%7Bs%3A8%3A%22currency%22%3Bs%3A3%3A%22rur%22%3Bs%3A5%3A%22limit%22%3Bi%3A20%3Bs%3A4%3A%22sort%22%3Ba%3A16%3A%7Bs%3A2%3A%22id%22%3BN%3Bs%3A4%3A%22date%22%3BN%3Bs%3A14%3A%22date_and_price%22%3BN%3Bs%3A10%3A%22mark_model%22%3BN%3Bs%3A4%3A%22year%22%3BN%3Bs%3A10%3A%22horsepower%22%3BN%3Bs%3A12%3A%22transmission%22%3BN%3Bs%3A6%3A%22engine%22%3BN%3Bs%3A8%3A%22capacity%22%3BN%3Bs%3A11%3A%22engine_type%22%3BN%3Bs%3A5%3A%22wheel%22%3BN%3Bs%3A4%3A%22city%22%3BN%3Bs%3A8%3A%22run_size%22%3BN%3Bs%3A4%3A%22gear%22%3BN%3Bs%3A5%3A%22price%22%3BN%3Bs%3A11%3A%22views_total%22%3BN%3B%7D%7D; search_offers=a%3A0%3A%7B%7D; search_window=table; presentationListHide=true; __utmt=1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'}
    r=requests.get(url, headers=header)
    if r.status_code != 200: return None
    res={}
    
    def find_param(regexp, text):
        match = re.search(regexp,text)
        if match:
            i,j = match.span()
            s=text[i:j-1]
            return s[s.rfind(">")+1:]
        return None
    
    res['id'] = url[url.rfind("/")+1:]
    
    # ---- title
    res['title']=find_param("au-offer-card__header-title-text.+?<", r.text)
    
    # ---- city
    res['city']=find_param(r"Характеристики.+?[Гг]ород.+?au-offer-card__tech-txt.+?<", r.text)
    
    # ---- price
    res['price']=find_param(r"Характеристики.+?[Цц]ена.+?au-offer-card__tech-txt.+?strong.+?<", r.text)
    
    # ---- phone
    res['phone']=e1_auto_phone_number(int(res['id']))
    
    return res
    
    
def main():
    for url in ["http://auto.e1.ru/car/used/opel/opel_astra/7511983",
                "http://auto.e1.ru/car/used/daewoo/espero/7819237",
                "http://auto.e1.ru/car/used/toyota/corolla/7794958"]:
        print(e1_auto_info(url))

if __name__ == "__main__":
    main()

