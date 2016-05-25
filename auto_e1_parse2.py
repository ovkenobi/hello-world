import re

def __find_param(pattern, text):
    match = re.search(pattern, text)
    if match:
        i,j = match.span()
        text=text[i:j-1]
        return text[text.rfind(">")+1:]
    return None


def all_href_car(text):
    for link in re.findall("au-elements__title__link_table.+?>", text, re.DOTALL):
        match=re.search("href=[\'\"].+?[\'\"]", link)
        if match:
            i,j=match.span()
            yield "http://auto.e1.ru"+link[i+6:j-1]

def get_public_info(text):
    res = {}
    # ---- id
    id = None
    match = re.search("og:url.+?>", text)
    if match:
        i,j = match.span()
        id = text[i:j-1]
        match = re.search(r"\d{4,}", id)
        if match:
            i,j = match.span()
            id = id[i:j]
    res['id'] = id

    text = text[text.find('au-offer-card__header-title-text'):-1000]
    
    # ---- title
    res['title']=__find_param("au-offer-card__header-title-text.+?<", text)

    text = text[text.find("Характеристики"):]
    # ---- city
    res['city']=__find_param(r"Характеристики.+?Город.+?au-offer-card__tech-txt.+?<", text)
    # ---- price
    res['price']=__find_param(r"Характеристики.+?Цена.+?au-offer-card__tech-txt.+?strong.+?<", text)
    if res['price']: res['price'] = res['price'].replace("&nbsp;",'')
    return res

def get_private_info(text):
    res = {}
    if 'error' not in text:
        res["phone"] = __find_param("au-offer-card__contacts-phone-txt.+?<", text)
        note = __find_param("au-offer-card__contacts-phone-notice.+?>", text)
        if note and "title" in note: res['note'] = note[note.rfind('title')+7:-1]
    return res

def main():
    all_href_car("asdasd")
    print(get_private_info(
    '''
<div class="au-offer-card__contacts-wrap _contacts_wrap">
                    <div class="au-offer-card__contacts _offer_contacts   au-offer-card__contacts_opened" data-offer_id="7814946" data-context="card"><div class="au-offer-card__contacts-inner _contacts"><div class="au-offer-card__contacts-box"><h3 class="au-offer-card__contacts-title">Контакты продавца</h3><div class="au-offer-card__contacts-block au-offer-card__contacts-block_box"><span class="au-offer-card__contacts-phone"><span class="au-offer-card__contacts-phone-txt">+7-961-762-02-42</span><span class="au-offer-card__contacts-phone-notice" title="Продавец"></span></span></div><div class="au-offer-card__contacts-block au-offer-card__contacts-block_question"><a href="" class="au-offer-card__contacts-link au-offer-card__contacts-link_dotted _question_link" data-tab="_questions"><span class="au-offer-card__contacts-txt">Задать вопрос продавцу</span></a></div><div class="au-offer-card__contacts-block au-offer-card__contacts-block_mail au-offer-card__contacts-mail"><a class="au-offer-card__contacts-link au-offer-card__contacts-link_dotted _send_seller_mail" href="javascript:void(null);" data-offer_id="7814946"><span class="au-offer-card__contacts-txt">Отправить письмо</span></a></div><div class="au-offer-card__contacts-block"><a href="" class="au-offer-card__contacts-link au-offer-card__contacts-link_dotted _offer_sold_link"><span class="au-offer-card__contacts-txt">Сообщить, что авто продано</span></a><span class="au-offer-card__contacts-txt au-offer-card__contacts-txt_sold _sold_msg hidden">Объявление будет проверено</span><div class="_offer_sold_title hidden">Вы позвонили и продавец подтвердил, что авто продано?</div><div class="_offer_sold_content hidden"><button class="au-flat-button au-offer-card__contacts-button _sold_btn_approve" data-id="7814946">Да</button><button class="au-flat-button au-offer-card__contacts-button _sold_btn_reset">Нет</button></div></div></div><div class="au-offer-card__contacts-box">

                                                                                </div>
            </div>
            </div>


            <div class="au-offer-card__velum"><ul class="au-offer-card__velums-list"><li class="au-offer-card__velums-item velum">
<script src="//reklama3.ngs.ru/ap-js/?pid=30222&amp;sn=auto.e1.ru&amp;ru=car&amp;ts=1464172017&amp;avc=7&amp;doh=10&amp;s=f3d09d8f740703bb14228f7c0c714ca4"></script><a target="_blank" class="au-flat-button au-flat-button-green-bright au-offer-card__velums-button" href="//reklama2.ngs.ru/kqpxznqyqw_pa-c5qn8rpeckoissjl5thm2sg?cb=2662639651">Купить любой авто в кредит от 250 000 р.</a><img src="//reklama2.ngs.ru/kqpxznqyqw/tpx?30222&amp;&amp;1464172018&amp;7138b59&amp;c5qn8rpeckoissjl5thm2sg&amp;2662639651" style="display: block; position: absolute;" alt="" height="1" width="1">
</li><li class="au-offer-card__velums-item velum">
<script src="//reklama1.ngs.ru/ap-js/?pid=30232&amp;sn=auto.e1.ru&amp;ru=car&amp;ts=1464172017&amp;avc=7&amp;doh=10&amp;s=f3505a71e95e392add5e9076398d0b1c"></script><a target="_blank" class="au-flat-button au-flat-button-green-bright au-offer-card__velums-button" href="//reklama2.ngs.ru/kpzwczxztj__rq-c5qn8rpeckoissjl5thm2sg?cb=1861245105"> Получи ДЕНЬГИ ПРОСТО под залог ПТС
</a><img src="//reklama2.ngs.ru/kpzwczxztj/tpx?30232&amp;&amp;1464172018&amp;5598dae8&amp;c5qn8rpeckoissjl5thm2sg&amp;1861245105" style="display: block; position: absolute;" alt="" height="1" width="1">
</li></ul></div>
    
                </div>
                '''))
    print(get_private_info("""<div class="au-offer-card__contacts-block au-offer-card__contacts-block_box"> \
<span class="au-offer-card__contacts-phone"><span class="au-offer-card__contacts-phone-txt">+7-961-762-02-42</span> \
 </span></div>                         """))
    
if __name__ == "__main__":
    main()
