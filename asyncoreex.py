import eventlet
from eventlet.green import urllib2
import time

from multiprocessing import Pool, Lock, Manager
import multiprocessing
import requests
import settings
import random

from bs4 import BeautifulSoup


import grequests
import time
from datetime import datetime


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print "{}: {}".format(datetime.now(), msg)
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text

def saved_proxy_paid():
    f = open('proxylist.csv','r')
    text = f.readlines()
    freshproxlist = []
    for line in text:
        prox ={
            'http':'http://sk004:cpUGUJ4L@{}:{}/'.format(line.strip(),60099),
            'https':'https://sk004:cpUGUJ4L@{}:{}/'.format(line.strip(),60099)
            }
        freshproxlist.append( prox )
    f.close()
    return freshproxlist

def fetch(r, *args, **kwargs):
    print (r.status_code,len(r.content))
    
def print_url(r, *args, **kwargs):
    print(r.url)

    

if __name__ == '__main__':


    f = open('isbns.txt','r')
    lines = f.readlines()
    isbns = []
    log("Reading URLS ... ")
    for line in lines:
        isbn = line.strip()
        isbns.append(isbn)
    f.close()

    ##Divides isbns into chunks
    divider = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    isbnschunklist = divider(isbns,10)
    urls = []
    for isbnchunk in isbnschunklist:
        isbnchunk = "%7C".join(isbnchunk)
        url = "https://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-isbn=" + isbnchunk + "&field-dateop=During&sort=relevanceexprank"
        urls.append(url)

    urls = urls[0:500]
    

##    start = time.time()
##    p = Pool(8)
##    result = p.map(fetch,urls,chunksize=1)
##    p.close()
##    p.join()
##    print "Run time  multiprocessing was: {}".format(time.time()-start)


    start = time.time()
    proxs = saved_proxy_paid()
    rs = (grequests.get(url , headers = headers , proxies = random.choice(proxs), timeout = (1,5) , hooks = dict(response=fetch)) for url in urls)
    ##Send the stack
    responses = grequests.map(rs, size = 50)
    print responses
    count = 0

    print count
    print "Running time: {}s".format(time.time()-start)
