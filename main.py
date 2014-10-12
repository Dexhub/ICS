from bs4 import BeautifulSoup, SoupStrainer
import requests
import xlsxwriter
from config import *
import sys
import pyprind as ppr
from database import Database
from company_data import Company_data
import signal
import sys
from Queue import Queue
from threading import Thread

## Global list of urls to be parsed
url_list = []
counter = 0
worksheet = None
db = None
main_queue = None


def signal_handler(signal, frame):
    print ("You pressed Ctrl+ C")
    exit(0)

def generate_urls(init_url):
    '''
    Parse the main url and add the links in the list
    Store the parsed data and call parsing until list is empty
    '''
    global url_list
    url_list.append(init_url)

    counter = 0
    while (counter < len(url_list)):
        url_to_parse = url_list[counter]
        counter = counter + 1
        if (counter > 4): #TODO
            break   
        extract_urls(url_to_parse)
        print('>'),
        sys.stdout.flush()

    print "-"*20
    print "Total number of results returned : %d" % (counter)
    print "-"*20

def extract_urls(url_to_parse):
    ''' Generate only the list of URLs to be parsed. This would help in creating a progress bar.'''
    #TODO Use Soup Strainer
    global main_queue
    r = requests.get(url_to_parse)                                                           
    only_footer_elements = SoupStrainer(id="FooterPageNav")
    soup = BeautifulSoup(r.content, parse_only = only_footer_elements)
    next_links = soup.find_all('li', {"class": "page notranslate"})
    for nl in next_links:
        a = nl.find('a')['href']
        nl = BASE_SITE + a
        if nl not in url_list:
            url_list.append(nl)
            main_queue.put(nl)

def begin_data_extraction(minimum):
    ''' Parse the url for actual data'''
    global url_list
    mbar = ppr.ProgBar(len(url_list))
    for url in url_list:
        parse(minimum)
        #parse(url, minimum)
        mbar.update()

def parse( minimum = 0):
    global main_queue
    url_to_parse = main_queue.get()
    r = requests.get(url_to_parse)                                                           
    soup = BeautifulSoup(r.content)
    # Company Names
    Companies = soup.find_all('a', {"class": "item org emphasizedLink"}) 
    
    # Company Ratings
    Ratings = soup.find_all("span", {"class": "gdRatingValueBar"}) 
   
    # Company headquaters
    HeadQuaters = soup.find_all("span", {"class": "hqInfo adr"}) 

    # Company Size
    # Company CEO
    CEOs = soup.find_all("p", {"class": "ceoData"}) 

    # Founding Date: Growth %
    #print "%d %d %d %d" % (len(Companies), len(Ratings), len(HeadQuaters), len(CEOs))

    ###############################
    global counter,db
    for i in range(0,len(Companies)):
        if(float(Ratings[i].text) > minimum):
            counter = counter + 1
            try:
                CEO = CEOs[i].find("span", {"class":"fn notranslate"}).text
            except:
                CEO = None
            try:
                HQ = HeadQuaters[i].find("span", {"class" : "value i-loc"}).text
            except:
                HQ = None
        
            try:
                approval = CEOs[i].find("span", {"class": "approvalPercent"}).text[:-1]
            except:
                approval = None
        
    
            # Code to insert Data
            Company = Company_data(Companies[i].text, \
                                   Companies[i].get('href'), \
                                   Ratings[i].text.strip(), \
                                   HQ, \
                                   CEO, \
                                   approval) 
            db.store(Company)
            Company.more_info()
    main_queue.task_done()


def main():
    global db, main_queue
    url = SEED_URL
    signal.signal(signal.SIGINT, signal_handler) # Yet to implement
    db = Database()
    main_queue = Queue()
    for i in range(NUM_WORKER_THREADS):
        t = Thread(target = parse)
        t.daemon = True
        t.start()
    minimum = input("What is the minimum rating of the companies you are searching for: ")
    print "Parsing Glassdoor in Real time .... Please be Patient"
    generate_urls(url)
    print "Finished Generating URLS"
    main_queue.join()
    #begin_data_extraction(minimum)
main()
