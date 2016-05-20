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
    
    # ---- title
    res['title']=__find_param("au-offer-card__header-title-text.+?<", text)
    # ---- city
    res['city']=__find_param(r"Характеристики.+?[Гг]ород.+?au-offer-card__tech-txt.+?<", text)
    # ---- price
    res['price']=__find_param(r"Характеристики.+?[Цц]ена.+?au-offer-card__tech-txt.+?strong.+?<", text)
    if res['price']: res['price'] = res['price'].replace("&nbsp;",'')
    return res

def get_private_info(text):
    res = {}
    if 'error' not in text:
        res["phone"] = __find_param("au-offer-card__contacts-phone-txt.+?<", text)
    return res

def main():
    all_href_car("asdasd")
    
if __name__ == "__main__":
    main()
