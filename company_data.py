from bs4 import BeautifulSoup
import requests
import xlsxwriter
from glassdoor import get
import threading 
from config import *

class Company_data():
    ''' This Class is used to store company general data and certain urls from which further information can be fetched. '''
    def __init__(self, name, url, rating = "0", HQ = "unknown", CEO = "unknown", approval = 0):
        self.name = name
        self.url = BASE_SITE + url
        print "URL : ", self.url
        self.rating = rating
        try:
            self.HQcity = HQ.split(',')[0].strip()
        except:
            self.HQcity = "unknown"
        try:
            self.HQstate = HQ.split(',')[1].strip()
        except:
            self.HQstate = "unknown"
        self.CEO = CEO
        self.approval = approval

    def more_info():
         info = get(self.name)
         print info

    def get_jobs():
        '''Get Jobs '''
        pass

    def push_db():
        ''' Save the information in database '''
        pass

    def get_company_info():
        ''' Get information about the company's work '''
        pass


class get_more_info(threading.Thread):
    def __init__(self, name, url):
        self.name = company_name

    def run(self):
        ''' Get all the job information and also get all office locations '''
        r = requests.get(url_to_parse)                                                           
        soup = BeautifulSoup(r.content)

        founded  = 
        size =
        company_type = 
        company_industry = 
        competitors = 
        summary =
        jobs_url
        locations from jobs_url
        next_links = soup.find_all('li', {"class": "page notranslate"})
        soup = 
        jobs_list = parse_all(self.name)
        locations = get_locations(jobs_list)




def parse_all(company_name):
    BASE_SITE = "http://www.glassdoor.com"
