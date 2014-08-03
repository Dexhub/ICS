''' Handles all the database related functions '''
from pymongo import MongoClient

class Database(object):
    company_data = None

    def __init__(self):
        ''' create a database if it does not exist and establish a connection '''
        client = MongoClient('localhost', 27017)
        db = client['glass']
        Database.company_data = db.company_data # creating a collection for company_data

    def store(this, company):
        ''' store the values set in the company_data object into the database '''
        Database.company_data.insert( \
                           { "Name" : company.name, \
                             "URL" : company.url, \
                             "Rating" : company.rating, \
                             "HQ city" : company.HQcity, \
                             "HQ state" : company.HQstate, \
                             "CEO" : company.CEO, \
                             "Approval" : company.approval, \
                           } \
                           )

    def query_rating():
        ''' query companies based on their ratings '''
        pass

    def store_job_info():
        ''' Store information regarding available jobs '''
        pass

    def query_location():
        ''' query companies based on their location '''
        pass
