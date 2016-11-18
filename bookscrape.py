from multiprocessing import Pool, Lock, Manager
import multiprocessing
import time
import urllib
import requests
import sys
import random
import os
from requests.exceptions import *
from functools import partial
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import *
from datetime import datetime
import settings



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

def get_proxy_saved():
    f = open('proxies.txt','r')
    text = f.readlines()
    freshproxlist = []
    for line in text:
        prox =  {
                'http':'http://'+ line.strip() +'/' ,
                'https':'https://'+ line.strip() +'/'
                }
        freshproxlist.append( prox )
    f.close()
    return freshproxlist

def get_proxy():
    ports = ['8080','80','3128','8888','81']
    proxlst = []
    proxycleanlst = []
    
    for port in tqdm(ports):
        url = 'http://gatherproxy.com/embed/?t=Elite&p=' + port + '&c='
        proxlst_saved = saved_proxy_paid()
        while True:
            try:
                prox  = random.choice(proxlst_saved)
                response = requests.get(url, headers=settings.headers, proxies = prox, timeout = (1,5))
                if response.status_code != 200:
                    print "Status code is not 200"
                    pass
                break
            except:
                print "Something wrong grabbing proxies"

        
        html = response.content
        print (len(html))
        soup = BeautifulSoup(html,'html.parser')
        try:
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})[3:len(proxlstraw)-3]
        except: print "Something wrong during scriping proxies from gatherproxy"
            
        
        for proxraw in proxlstraw:
            proxraw = unicode(proxraw.string).strip()
            beg = '"PROXY_IP":"'
            end = '","PROXY_LAST_UPDATE":'
            try:
                proxclean =  proxraw[proxraw.index(beg)+len(beg):proxraw.index(end)] + ':' + port
                proxlst.append({
                    'http':'http://' + str(proxclean),
                    'https':'https://' + str(proxclean)
                    })
                proxycleanlst.append(proxclean)
            except: print "proxclean not properly read: Error arising from get_proxy()"
            
    for port in tqdm(ports):
        url = 'http://gatherproxy.com/embed/?t=Transparent&p=' + port + '&c='
        proxlst_saved = saved_proxy_paid()
        while True:
            try:
                prox  = random.choice(proxlst_saved)
                response = requests.get(url, headers=settings.headers, proxies = prox, timeout = (1,5))
                if response.status_code != 200:
                    print "Status code is not 200"
                    pass
                break
            except:
                print "Something wrong grabbing proxies"

        
        html = response.content
        print (len(html))
        soup = BeautifulSoup(html,'html.parser')
        try:
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})
            proxlstraw = soup.find_all('script',attrs={'type':'text/javascript'})[3:len(proxlstraw)-3]
        except: print "Something wrong during scriping proxies from gatherproxy"
            
        
        for proxraw in proxlstraw:
            proxraw = unicode(proxraw.string).strip()
            beg = '"PROXY_IP":"'
            end = '","PROXY_LAST_UPDATE":'
            try:
                proxclean =  proxraw[proxraw.index(beg)+len(beg):proxraw.index(end)] + ':' + port
                proxlst.append({
                    'http':'http://' + str(proxclean),
                    'https':'https://' + str(proxclean)
                    })
                proxycleanlst.append(proxclean)
            except: print "proxclean not properly read: Error arising from get_proxy()"

    f = open('proxies.txt','w')
    for proxy in proxycleanlst: f.write(proxy +'\n')
    f.close
    return proxlst

proxylist = get_proxy()



#*#Goes into the directory defined by path, and obtains names + extention of all files in the directory.        
def filename_extractor(path):
    lst = []
    files = os.listdir(path)
    for filename in files: lst.append(filename[:len(filename)-4])
    return lst

def log(msg):
    # global logging function
    if settings.log_stdout:
        try:
            print "{}: {}".format(datetime.now(), msg)
        except UnicodeEncodeError:
            pass  # squash logging errors in case of non-ascii text


def get_tiv(soup):
    ## Trade-In locator
    tradeinbutton = soup.find('div',attrs={'id':'tradeInButton'})
    if not tradeinbutton:
        log('TIV not found. DNE')
        tiv = 0
        return tiv
    else:
        tradeinbutton = tradeinbutton.text
        tiv = float(re.findall('\$(\d+\.\d+)*',tradeinbutton)[0].replace(',','').replace('$',''))
        log('TIV Found: {}'.format(tiv))
        return tiv


def get_price(soup):
    ## Used Price Locator
    pricebox = soup.find('li',attrs={'class':'swatchElement selected'})
    if not pricebox:
        morebuyingchoices = soup.find('div',attrs={'id':'mediaOlp'})
        if not morebuyingchoices:
            log("More Buying Choices box not found")
            usedprice = None
            newprice = None
        prices = morebuyingchoices.find_all('span',attrs={'class':'olp-padding-right'})
        for price in prices:
            condition =  price.find('a').string
            if 'used' in condition.lower():
                usedpricelowest = price.find('span','a-color-price').string
                usedpricelowest = float(re.findall('\$(\d+\.\d+)*',usedpricelowest)[0].replace(',','').replace('$',''))
                log('Lowest Used Price found: {}'.format(usedpricelowest))
            elif 'new' in condition.lower():
                newpricelowest = price.find('span','a-color-price').string
                newpricelowest = float(re.findall('\$(\d+\.\d+)*',newpricelowest)[0].replace(',','').replace('$',''))
                log('Lowest New Price found: {}'.format(newpricelowest))
            else: pass
        if not usedpricelowest:
            usedpricelowest = 934393439343
            log('No lowest used price found')
        if not newpricelowest:
            newpricelowest = 934393439343
            log('No lowest used price found')
        return (usedpricelowest,newpricelowest)
    
    usedpricelowest = pricebox.find('span',attrs={'class':'olp-used olp-link'})
    if not usedpricelowest:
        usedpricelowest = 934393439343
        log('No lowest used price found')

    usedpricelowest = str(usedpricelowest.text)
    usedpricelowest = float(re.findall('\$(\d+\.\d+)*',usedpricelowest)[0].replace(',','').replace('$',''))

    
    newpricelowest = pricebox.find('span',attrs={'class':'olp-new olp-link'})
    if not newpricelowest:
        newpricelowest = 934393439343
        log('No lowest new price found')
    newpricelowest = str(newpricelowest.text)
    newpricelowest = float(re.findall('\$(\d+\.\d+)*',newpricelowest)[0].replace(',','').replace('$',''))
    
    return (usedpricelowest,newpricelowest)


def make_request(url):
    global proxylist
    while True:
        try:
            proxy = random.choice(proxylist)
            response = requests.get(url, headers = settings.headers, proxies = proxy, timeout = (2,10))
            html = response.content
            if len(html) < 10000:
                log('Failure! Less than 1000, {} len(html) {} Retrying ...'.format(proxy,len(html)))
                continue
            break
        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
            log('Failure! {} Exception raised. Retrying ...'.format(proxy))
    log('Success! {} len(html) {}'.format(proxy,len(html)))
    soup = BeautifulSoup(html,'html.parser')

    tiv = get_tiv(soup)
    (usedprice,newprice) = get_price(soup)
    log('{}, {}, {}'.format(tiv, usedprice, newprice))
    return (tiv, usedprice, newprice)



        

if __name__ == '__main__':
    
    f = open('isbns.txt','r')
    lines = f.readlines()
    urls = []
    log("Reading URLS ... ")
    for line in lines:
        url = "https://www.amazon.com/gp/product/" + line.strip()
        urls.append(url)
    f.close()
    
    urls = urls[0:10]

    start = time.time()
    p = Pool(4)
    log("Started scraping process ... ")
    result = p.map(make_request,urls)
    print result
    p.close()
    p.join() 
    print 'Runtime: %ss' % (time.time()-start)
