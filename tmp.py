from urllib import request

def load_page(iter_links, iter_proxy):
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
            yield text

#asdas			
def request_post(url, proxy, body, headers=None):
	if headers is None: headers={}
	headers['Content-Length'] = len(body)
	opener = request.build_opener(proxy)
	opener.addheaders=headers
	# method
	# set body
	try:
		r = opener.open(url, timeout=30)
	