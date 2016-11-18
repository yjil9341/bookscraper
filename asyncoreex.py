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


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
}

def fetch(url):
    html = requests.get(url , headers = headers ).content
    print url
    return None
##    soup = BeautifulSoup(html,'html.parser')
##    print "Soup Found"
##    return soup

def print_url(r, *args, **kwargs):
    print(r.url)

if __name__ == '__main__':
    
    urls = [
        'http://www.heroku.com',
        'http://www.tablib.org',
        'http://www.httpbin.org',
        'http://www.python-requests.org',
        'http://www.kennethreitz.com'
    ]

    urls = urls*100

##    start = time.time()
##    p = Pool(8)
##    result = p.map(fetch,urls,chunksize=1)
##    p.close()
##    p.join()
##    print "Run time  multiprocessing was: {}".format(time.time()-start)


    start = time.time()
    rs = (grequests.get(url , headers = headers , timeout = (1,5) , hooks = dict(response=print_url)) for url in urls)
    ##Send the stack
    responses = grequests.map(rs, size = 50)
    print responses
    count = 0
##    for response in responses:
##        html = response.content
##        soup = BeautifulSoup(html,'html.parser')
##        print "Soup Found"
##        response.close
##        count += 1
    print count
    print "Running time: {}s".format(time.time()-start)
