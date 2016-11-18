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


import grequests
import time


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

proxylist = saved_proxy_paid()


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

    try: itemboxes = soup.find_all('li', attrs = {'class':'s-result-item celwidget'})
    except: print "There was something wrong with reading individual items"

    for itembox in itemboxes:
        ## Get title and Item Link
        titlelink = itembox.find('a',attrs={'class':'s-access-detail-page'})
        if not titlelink:
            title = "No Title"
            link = "No Link Found"
            print title, link 
        title = titlelink.get('title')
        title = unicode(title).encode('ascii','ignore')
        itemlink = titlelink.get('href')
        itemlink = unicode(itemlink).encode('ascii','ignore')


        ##Get Selling Price
        pricecontainer = itembox.find('div',attrs={'class':'a-column a-span7'})
        if not pricecontainer:
            log("No price box found")
            price = 0
        prices = pricecontainer.find_all('a',attrs={'class':'a-size-small a-link-normal a-text-normal'})
        for price in prices:
            print price

        pricecontainer = itembox.find('div',attrs={'class':'a-column a-span5 a-span-last'})
        if not pricecontainer:
            log("No TIV box found")
            tiv = 0
            return        
        tiv = pricecontainer.find('a',attrs={'class':'a-color-price'})
        print tiv
        print tiv.string

    return None


def get_title_link(itembox):
    titlelink = itembox.find('a',attrs={'class':'s-access-detail-page'})
    if not titlelink:
        title = "No Title"
        itemlink = "No Link Found"
##        log("{}{}".format(title,itemlink))
        return (title,itemlink)
    title = titlelink.get('title')
    title = unicode(title).encode('ascii','ignore')
    itemlink = titlelink.get('href')
    itemlink = unicode(itemlink).encode('ascii','ignore')
##    log(title)
    return (title,itemlink)

def get_tiv(itembox):
    pricecontainer = itembox.find('div',attrs={'class':'a-column a-span5 a-span-last'})
    if not pricecontainer:
##        log("No TIV box found")
        tiv = 0
        tiv = str(tiv)
        return tiv
    tiv = pricecontainer.find('span',attrs={'class':'a-color-price'})
    if not tiv:
        tiv = 0
        tiv = str(tiv)
##        log("TIV box found. No TIV value ${}".format(tiv))
        return tiv
    tiv =  tiv.string
    tiv = tiv.replace('$','')
##    tiv = float(re.findall('\$(\d+\.\d+)*',tiv)[0].replace(',','').replace('$',''))
##    log("TIV found {}".format(tiv))
    return tiv


def get_price(itembox):
    ##Get Selling Price
    pricecontainer = itembox.find('div',attrs={'class':'a-column a-span7'})
    if not pricecontainer:
##        log("No price box found")
        price = 99999
        price = str(price)
        return price
    ## Could be the case that there maybe multiple prices. Need to fix this
##    price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-price a-text-bold'})
    price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-base'})
    if not price:
        price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-price a-text-bold'})
    if not price:
        price = pricecontainer.find('span',attrs={'class':'a-size-base a-color-price'})
    if not price:
##        log('Price box found. No prices found. $0')
        price = 99999
        price = str(price)
        return price
    
    price =  price.string
    price = price.replace('$','')
##    price = float(re.findall('\$(\d+\.\d+)*',price)[0].replace(',','').replace('$',''))
##    log('Price found. {}'.format(price))
    return price

def get_asin(itembox):
    asin = itembox.get('data-asin')
    if not asin:
        asin = "0000000000"
##        log('ASIN not found {}'.format(asin))
        return asin
##    log('ASIN Found {}'.format(asin))
    asin = str(asin)
    return asin
    

def make_request_test(url):
    global proxylist
    while True:
        try:
            proxy = random.choice(proxylist)
            response = requests.get(url, headers = settings.headers ,proxies=proxy, timeout = (1,5))
            html = response.content
            if len(html) < 10000:
                log('Failure! Less than 1000, {} len(html) {} Retrying ...'.format(proxy,len(html)))
                continue
            break
        except (ConnectTimeout,ReadTimeout,ChunkedEncodingError,ProxyError,ConnectionError,ContentDecodingError,TooManyRedirects):
            log('Failure! {} Exception raised. Retrying ...'.format(proxy))
    log('Success! {} len(html) {}'.format(proxy,len(html)))
    soup = BeautifulSoup(html,'html.parser')

    itemboxes = soup.find_all('li', attrs = {'class':'s-result-item celwidget'})
    if itemboxes == []:
        print "There was something wrong with reading individual items"
        return None

    for itembox in itemboxes:
        title,itemlink = get_title_link(itembox)
        asin = get_asin(itembox)
        tiv = get_tiv(itembox)
        price = get_price(itembox)
    return [asin,tiv,price]



##def fetch_url(url,sharedproxs):
##    data = []
##    url = format_url(url)
##    soup = proxy_loop(url,sharedproxs[0])
##    
##    #Grabs all rows containing a book.
##    count = 0
####    print "Soup type: %s" %soup
##    try: divs = soup.find_all('li', attrs = {'class':'s-result-item celwidget'})
##    except: print "There was something wrong with reading individual items"
##
##
##        
##
##        if div.find_all('span',attrs={'class':'a-size-base a-color-price a-text-bold'}) == []:
##            ## This could be a wrong way to detect tradeinprice, check this later
##            price = 0.001
##        else:
##            try: priceraw =  div.find_all('span',attrs={'class':'a-size-base a-color-price a-text-bold'})[0].contents[0]
##            except: print "something wrong with printing price raw"
##            price = float(re.findall('\$(.+)*',priceraw)[0].replace(',','').replace('$',''))
##
##        try: isbn = div.get('data-asin')
##        except:
##            print 'isbn not properly read'
##            sys.exit()
##            
##        tradeinpricebox =  div.find('div',attrs={'class':'a-column a-span5 a-span-last'})
##        if tradeinpricebox.find('span',attrs={'class':'a-color-price'}) == None:
##            ## This could be a wrong way to detect tradeinprice, check this later
##            tradeinprice = 0
##        else:
##            try:
##                tradeinpricebox = tradeinpricebox.find('div',attrs={'class':'a-row a-spacing-none'})
##                tradeinprice = tradeinpricebox.find('span',attrs={'class':'a-color-price'}).contents[0]
##                tradeinprice = float(re.findall('\$(.+)*',tradeinprice)[0].replace(',','').replace('$',''))
##            except:
##                print "No trade-in price detected"
##                tradeinprice = 0
##                print price , tradeinprice, isbn
##                
##            
##        
##        priceofferslink =  "https://www.amazon.com/gp/offer-listing/"+ str(isbn) +"/ref=olp_f_usedAcceptable?ie=UTF8&f_new=true&f_usedGood=true&f_usedLikeNew=true&f_usedVeryGood=true&overridePriceSuppression=1&sort=taxsip"
##        
##        ## If tradeinprice exists, we will try to save it to a file.
##        ## This is shared between multiuple multiprocessing mtretretrelMake a list of odules
##        if tradeinprice == 0: continue
##        else: pass
##        
##        if tradeinprice > 10: sharedproxs[1].append(isbn)
##        else: pass
##
##        
##        
##        profit = tradeinprice - (price + 3.99)
##        if profit > 10:
##            count += 1
##            print profit , price , tradeinprice, isbn
##            print 'Checking if any items are profitable'
##            print priceofferslink
##            profitable_result = check_profitable(priceofferslink,sharedproxs[0], tradeinprice)
##            if profitable_result == []: return []
##            else: pass
##
##            print 'There exist at least one profitable item, appending the item to data'
##            titlehtml = '<a href="' + itemlink +'">' + title + '</a>'
##            titlehtml= unicode(titlehtml).encode('ascii','ignore')
##            isbncomparison = '<a href="http://www.bookfinder.com/buyback/search/#' + isbn + '">' + isbn + '</a>'
##            isbncomparison = unicode(isbncomparison).encode('ascii','ignore')
##            timestamp = datetime.datetime.now().strftime("%B %d %I:%M%p")
##            ## If profitable percentage is less than 15%, skip.
##            ## However the code fails to catch profit pargins that are for example 14% and prime (definately buyabke).
##            ## Needs to correct this later.
##
##            
##            print [titlehtml + ' ' + isbncomparison + ' ' + timestamp, '-----' , '-----', '-----', '-----', '-----' , '-----' ]
##            data.append([titlehtml + ' ' + isbncomparison + ' ' + timestamp, '-----' , '-----', '-----', '-----', '-----' , '-----' ])
##
##
##            countsub = 0
##            for lst in profitable_result:
##                if lst == []: continue
##                else:
##                    count += 1
##                    print lst
##                    data.append(lst)
##            if countsub == 0: print 'There was a difference in trade-in price, but no data has been added and printed'
##            else: pass
##        else: pass
##
##    #If the price doesn't meet the profitability cutoff, 
##    if count == 0:return []
##    else:return data

        

if __name__ == '__main__':
    
    f = open('isbns.txt','r')
    lines = f.readlines()
    isbns = []
    log("Reading URLS ... ")
    for line in lines:
        isbn = line.strip()
        isbns.append(isbn)
    f.close()

    divider = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    isbnschunklist = divider(isbns,10)
    urls = []
    for isbnchunk in isbnschunklist[0:5]:
        isbnchunk = "%7C".join(isbnchunk)
        url = "https://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-isbn=" + isbnchunk + "&field-dateop=During&sort=relevanceexprank"
        urls.append(url)

    start = time.time()
    p = Pool(4)
    log("Started scraping process ... ")
    result = p.map(make_request_test,urls)
    print result
    p.close()
    p.join() 
    print 'Runtime: %ss' % (time.time()-start)

##    print url
##    make_request_test(url)
