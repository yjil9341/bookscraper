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

##proxylist = saved_proxy_paid()
##proxylist = get_proxy()


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


##
##
##def make_request(url):
##    global proxylist
##    while True:
##        try:
##            proxy = random.choice(proxylist)
##            response = requests.get(url, headers = settings.headers, proxies = proxy, timeout = (2,10))
##            html = response.content
##            if len(html) < 10000:
##                log('Failure! Less than 1000, {} len(html) {} Retrying ...'.format(proxy,len(html)))
##                continue
##            break
##        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
##            log('Failure! {} Exception raised. Retrying ...'.format(proxy))
##    log('Success! {} len(html) {}'.format(proxy,len(html)))
##    soup = BeautifulSoup(html,'html.parser')
##
##    try: itemboxes = soup.find_all('li', attrs = {'class':'s-result-item celwidget'})
##    except: print "There was something wrong with reading individual items"
##
##    for itembox in itemboxes:
##        ## Get title and Item Link
##        titlelink = itembox.find('a',attrs={'class':'s-access-detail-page'})
##        if not titlelink:
##            title = "No Title"
##            link = "No Link Found"
##            print title, link 
##        title = titlelink.get('title')
##        title = unicode(title).encode('ascii','ignore')
##        itemlink = titlelink.get('href')
##        itemlink = unicode(itemlink).encode('ascii','ignore')
##
##
##        ##Get Selling Price
##        pricecontainer = itembox.find('div',attrs={'class':'a-column a-span7'})
##        if not pricecontainer:
##            log("No price box found")
##            price = 0
##        prices = pricecontainer.find_all('a',attrs={'class':'a-size-small a-link-normal a-text-normal'})
##        for price in prices:
##            print price
##
##        pricecontainer = itembox.find('div',attrs={'class':'a-column a-span5 a-span-last'})
##        if not pricecontainer:
##            log("No TIV box found")
##            tiv = 0
##            return        
##        tiv = pricecontainer.find('a',attrs={'class':'a-color-price'})
##        print tiv
##        print tiv.string
##
##    return None


def get_title_link(itembox):
    titlelink = itembox.find('a',attrs={'class':'s-access-detail-page'})
    if not titlelink:
        title = "No Title"
        itemlink = "No Link Found"
##        log("{}{}".format(title,itemlink))
        return (title,itemlink)

    itemlink = titlelink.get('href')
    itemlink = unicode(itemlink).encode('ascii','ignore')
    title = titlelink.get('title')
    title = unicode(title).encode('ascii','ignore')

##    log(title)
    return (title,itemlink)

def get_tiv(itembox):
    pricecontainer = itembox.find('div',attrs={'class':'a-column a-span5 a-span-last'})
    if not pricecontainer:
        tiv = 0
        tiv = float(tiv)
        return tiv
    tiv = pricecontainer.find('span',attrs={'class':'a-color-price'})
    if not tiv:
        tiv = 0
        tiv = float(tiv)
        return tiv
    tiv =  tiv.string
    tiv = float(tiv.replace('$','').replace(',',''))
    return tiv


def get_price(itembox):
    ##Get Selling Price
    pricecontainer = itembox.find('div',attrs={'class':'a-column a-span7'})
    if not pricecontainer:
        price = 99999
        price = float(price)
        return price
    ## Could be the case that there maybe multiple prices. Need to fix this
    price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-base'})
    if not price:
        price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-price a-text-bold'})
    if not price:
        price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-price'})
    if not price:
        price = 99999
        price = float(price)
        return price
    
    price =  price.string
    price = float(price.replace('$','').replace(',',''))
    return price

def get_asin(itembox):
    asin = itembox.get('data-asin')
    if not asin:
        asin = "0000000000"
        return asin
    asin = str(asin)
    return asin
    

def make_request_test(url,sharedproxs):
##    global proxylist
    while True:
        try:
            proxy = random.choice(sharedproxs)
            response = requests.get(url, headers = settings.headers ,proxies=proxy, timeout = (1,5))
            html = response.content
            if len(html) < 10000:
                if len(sharedproxs) == 0:
                    for proxy in get_proxy(): sharedproxs.append(proxy)
                else:
                    try: sharedproxs.remove(proxy)
                    except: pass
                log('Failure! {} Exception raised. Retrying ... len(sharedproxs) {}'.format(proxy,len(sharedproxs) ))
                continue
            break
        except (IndexError,UnboundLocalError):
            log('Index ERROR Exception raised. Retrying ... len(sharedproxs) {}'.format(len(sharedproxs) ))
            for proxy in get_proxy(): sharedproxs.append(proxy)
            
        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
            log('ERROR {} Exception raised. Retrying ... len(sharedproxs) {}'.format(proxy,len(sharedproxs) ))
            if len(sharedproxs) == 0:
                for proxy in get_proxy(): sharedproxs.append(proxy)
            else:
                try: sharedproxs.remove(proxy)
                except: pass
    log('Success! {} len(html) {} len(sharedproxs) {}'.format(proxy,len(html),len(sharedproxs)))
    soup = BeautifulSoup(html,'html.parser')

    itemboxes = soup.find_all('li', attrs = {'class':'s-result-item celwidget'})
    if itemboxes == []:
        print "There was something wrong with reading individual items"
        return [[]]
    resultcontainer = []
    for itembox in itemboxes:
        tiv = get_tiv(itembox)
        price = get_price(itembox)
        profit = tiv - price

        if profit < 10: continue
        else: pass

        title,itemlink = get_title_link(itembox)
        asin = get_asin(itembox)
        
        offerlink = "https://www.amazon.com/gp/offer-listing/"+ asin +"/ref=olp_f_usedAcceptable?ie=UTF8&f_new=true&f_usedGood=true&f_usedLikeNew=true&f_usedVeryGood=true&overridePriceSuppression=1&sort=taxsip"
        titlehtml = '<a href="' + itemlink +'">' + title + '</a>'
        titlehtml= unicode(titlehtml).encode('ascii','ignore')
        isbncomparison = '<a href="http://www.bookfinder.com/buyback/search/#' + asin + '">' + asin + '</a>'
        isbncomparison = unicode(isbncomparison).encode('ascii','ignore')
        resultcontainer.append([titlehtml,profit,tiv,price,isbncomparison ])
        
    return resultcontainer
        

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

    
    chunks = divider(urls,1000)
    count = 0
    absbegin = time.time()
    for chunk in chunks:
        start = time.time()
        
        proxs = get_proxy()
        p = Pool(8)
        manager = Manager()
        freshproxies = manager.list(proxs)

        log("Started scraping process ... ")
        partial_make_request_test = partial(make_request_test,sharedproxs = freshproxies)
        result = p.map(partial_make_request_test,chunk)

        
        refined_result = []
        for resultlst in result:
            if resultlst == [[]]: continue
            for booklst in resultlst:
                refined_result.append(booklst)

        p.close()
        p.join() 
        print 'Runtime: %ss' % (time.time()-start)

        count += 1
                
        df = pd.DataFrame(refined_result, columns=['Title','Profit' ,'TIV','Price','ASIN'])
        pd.set_option('display.max_colwidth', -1)
        df.to_html('isbn_amazon/' + str(count) +'.html',escape=False, index=False)
    print 'Runtime Total: %ss' % (time.time()- absbegin)
        
    


##    print url
##    make_request_test(url)
