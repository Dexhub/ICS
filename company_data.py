from bs4 import BeautifulSoup
import requests
import xilsxwriter
from glassdoor import get

class Company_data():
    ''' This Class is used to store company general data and certain urls from which further information can be fetched. '''
    def __init__(self, name, rating, HQ):
        self.name = name
        self.rating = rating
        self.HQ = HQ

    def more_info():
         info = get(self.name)
         print "-"*30
         print info
         print "-"*30

    def get_jobs():
        '''Get Jobs '''
        pass

    def push_db():
        ''' Save the information in database '''
        pass

    def get_company_info():
        ''' Get information about the company's work '''
        pass
