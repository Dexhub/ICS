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
        #print "URL : ", self.url
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
        self.more_info()

    def more_info(self):
        self.more = get_more_info(self)
        self.more.start()


    def save_info(size, founded, company_type, industry, revenue, competitors, numberOfReviews, numberOfSalaries, numberOfInterviews, companyDesc, jobsURL):
        self.size = size
        self.founded = founded
        self.company_type = company_type
        self.industry = industry
        self.revenue = revenue
        self.competitors = competitors
        self.numberOfReviews = numberOfReviews
        self.numberOfSalaries= numberOfSalaries
        self.numberOfInterviews = numberOfInterviews
        self.companyDesc = companyDesc
        self.companyMission = companyMission
        self.jobsURL = jobsURL

    def get_jobs():
        '''Get Jobs '''
        pass

    def push_db():
        ''' Save the information in database '''


    def get_company_info():
        ''' Get information about the company's work '''
        pass


class get_more_info(threading.Thread):
    def __init__(self, company):
        threading.Thread.__init__(self)
        self.url = company.url

    def run(self):
        ''' Get all the job information and also get all office locations '''
        r = requests.get(self.url)                                                           
        soup = BeautifulSoup(r.content)

        moreInfo = soup.find_all("span", {"class", "empData"})


        size = moreInfo[1].text.rsplit(' ', 1)[0] # Remove the word Employees appended at the end
        founded = moreInfo[2].text.strip()
        company_type = moreInfo[3].text.strip()
        industry = moreInfo[4].text.strip()
        revenue = moreInfo[5].strip()
        try:
            competitors = []
            competitors_links = moreInfo[6].find_all('a')
            for other_company in competitors_links:
                competitors.append({other_company.text, other_company.get('href')})
        except:
            competitors = []



        numberOfReviews = soup.find("a", {"class":"eiCell cell reviews "}).text.strip().rsplit(' ', 1)[0].strip()
        numberOfSalaries= soup.find("a", {"class":"eiCell cell salaries "}).text.strip().rsplit(' ', 1)[0].strip()
        numberOfInterviews = soup.find("a", {"class":"eiCell cell interviews "}).text.strip().rsplit(' ', 1)[0].strip()


        companyDesc = soup.find("p", {"id":"EmpDescription"}).text
        companyMission = soup.find("p", {"id":"EmpMission"}).text

        try:
            jobsURL = soup.find("a", {"class":"eiCell cell jobs"}).get('href')
        except:
            jobsURL = None

        ''' Get the locations of company offices based on jobs url '''

        # Save company information
        self.company.save_info(size, founded, company_type, industry, revenue, competitors, numberOfReviews, numberOfSalaries, numberOfInterviews, companyDesc, jobsURL)
        
def parse_all(company_name):
    BASE_SITE = "http://www.glassdoor.com"
