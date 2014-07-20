from bs4 import BeautifulSoup
import requests                                                                 
                

def parse_url(url):
    r = requests.get(url)                                                           
    soup = BeautifulSoup(r.content)
#    links = soup.find_all('a')                                                      
    g_data = soup.find_all('a', {"class": "item org emphasizedLink"}) 
    for data in g_data:
        print data.text



#Extracting the rating:                                                         
print "--"*5
#url = raw_input("Pilease enter a website name")                                
url = "http://www.glassdoor.com/Reviews/information-technology-reviews-SRCH_II10013.0,22"
next_url = "_IP"

print "#"*20
for N in range(2, 100):
    search_url = "%s%s%d.htm" %(url,next_url,N)
    print search_url
    parse_url(search_url)
print "#"*20

#http://www.glassdoor.com/Reviews/information-technology-company-reviews-SRCH_II10013.0,22_IP3.htm
