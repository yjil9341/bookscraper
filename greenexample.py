import eventlet
from eventlet.green import urllib2
import time

from multiprocessing import Pool, Lock, Manager
import multiprocessing
import requests
import settings
import random

def fetch(url):
    body = requests.get(url).content
    print("got body from", url, "of length", len(body)) 
    return None

if __name__ == '__main__':


    urls = [
        "https://www.google.com/intl/en_ALL/images/logo.gif",
        "http://python.org/images/python-logo.gif",
        "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif",
        "http://python.org/images/python-logo.gif",
        "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"
    ]

##    urls = urls*100
##    start = time.time()
##    pool = eventlet.GreenPool(settings.max_threads)
##    pile = eventlet.GreenPile(pool)
##    ##for url, body in pool.imap(fetch, urls):
##    ##    print("got body from", url, "of length", len(body))
##    ##print "Run time was: {}".format(time.time()-start)
##
##    [pile.spawn(fetch,url) for url in urls]
##    pool.waitall()

    urls = urls*100
    print len(urls)

    start = time.time()
    p = Pool(4)
    result = p.map(fetch,urls)
    p.close()
    p.join()
    print "Run time was: {}".format(time.time()-start)
