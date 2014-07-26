from bs4 import BeautifulSoup
import requests
import xlsxwriter
from config import *
import sys
import pyprind as ppr
from database_module import Database

## Global list of urls to be parsed
url_list = []
counter = 0
worksheet = None
db = None

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
        if (counter > 5):
            break
        extract_urls(url_to_parse)
        print('#'),
        sys.stdout.flush()

    print "-"*20
    print "Total number of results returned : %d" % (counter)
    print "-"*20

def extract_urls(url_to_parse):
    ''' Generate only the list of URLs to be parsed. This would help in creating a progress bar.'''
    #TODO Use Soup Strainer
    r = requests.get(url_to_parse)                                                           
    soup = BeautifulSoup(r.content)
    next_links = soup.find_all('li', {"class": "page notranslate"})
    for nl in next_links:
        a = nl.find('a')['href']
        nl = BASE_SITE + a
        if nl not in url_list:
            url_list.append(nl)

def begin_data_extraction(minimum):
    ''' Parse the url for actual data'''
    global url_list
    mbar = ppr.ProgBar(len(url_list))
    for url in url_list:
        parse(url, minimum)
        mbar.update()

def parse(url_to_parse, minimum):
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

    ###############################
    global counter
    for i in range(0,len(Companies)):
        if(float(Ratings[i].text) > minimum):
            counter = counter + 1
            '''
            try:
               print "%d %s %s %s %s %s " % \
                   (counter,\
                    Companies[i].text,\
                    Ratings[i].text,\
                    HeadQuaters[i].find("span", {"class" : "value i-loc"}).text,\
                    CEOs[i].find("span", {"class":"fn notranslate"}).text,\
                    CEOs[i].find("span", {"class": "approvalPercent"}).text[:-1])
            except:
                pass
            '''

def main():
    global db
    url = SEED_URL
    minimum = input("What is the minimum rating of the companies you are searching for:")
    generate_urls(url)
    db = Database()

    print "Finished Generating URLS"
    begin_data_extraction(minimum)
main()
