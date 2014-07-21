from bs4 import BeautifulSoup
import requests                                                                 
                
## Global list of urls to be parsed
url_list = []
site_name = "http://www.glassdoor.com"

def parse_url(url):
    '''
    Function adds the next links in the list of urls to be parsed.
    Parses the company details on the page and stores them in database.
    '''
    r = requests.get(url)                                                           
    soup = BeautifulSoup(r.content)
#    links = soup.find_all('a')                                                      
    g_data = soup.find_all('a', {"class": "item org emphasizedLink"}) 
    for data in g_data:
        print data.text
    rating_data = soup.find_all("span", {"class": "gdRatingValueBar"})
    for data in rating_data:
        print data.text


#
##Extracting the rating:                                                         
#print "--"*5
##url = raw_input("Pilease enter a website name")                                
#url = "http://www.glassdoor.com/Reviews/information-technology-reviews-SRCH_II10013.0,22"
#next_url = "_IP"
#
#print "#"*20
#for N in range(2, 3):
#    search_url = "%s%s%d.htm" %(url,next_url,N)
#    print search_url
#    parse_url(search_url)
#print "#"*20
#
def begin_parsing(init_url, minimum):

    '''
    Parse the main url and add the links in the list
    Store the parsed data and call parsing until list is empty
    '''
    global url_list
    url_list.append(init_url)


    counter = 0
    while counter < len(url_list):
        url_to_parse = url_list[counter]
        counter = counter + 1
        parse(url_to_parse, minimum)

    print "-"*10
    print url_list 

def parse(url_to_parse, minimum):
    global url_list
    r = requests.get(url_to_parse)                                                           
    soup = BeautifulSoup(r.content)
    next_links = soup.find_all('li', {"class": "page notranslate"})
    for nl in next_links:
        a = nl.find('a')['href']
        nl = site_name + a
        if nl not in url_list:
            url_list.append(nl)
    
    Companies = soup.find_all('a', {"class": "item org emphasizedLink"}) 
    Ratings = soup.find_all("span", {"class": "gdRatingValueBar"})
    for i in range(0,len(Companies)):
        if(float(Ratings[i].text) > minimum):
            print "> %s %s" % (Companies[i].text,Ratings[i].text)

def main():
    url = "http://www.glassdoor.com/Reviews/information-technology-reviews-SRCH_II10013.0,22.htm"
    minimum = input("What is the minimum rating of the companies you are searching for:")
    begin_parsing(url, minimum)

#http://www.glassdoor.com/Reviews/information-technology-company-reviews-SRCH_II10013.0,22_IP3.htm

main()
