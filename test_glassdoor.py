from bs4 import BeautifulSoup
import requests
import xlsxwriter
                
## Global list of urls to be parsed
url_list = []
site_name = "http://www.glassdoor.com"
counter = 0
worksheet = None

def begin_parsing(init_url, minimum):

    '''
    Parse the main url and add the links in the list
    Store the parsed data and call parsing until list is empty
    '''
    global url_list, worksheet
    url_list.append(init_url)
    
    ## Write Data to Excel Sheet ##
    workbook = xlsxwriter.Workbook('demo.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    # Writing Columns
    worksheet.write('A1', 'No', bold)
    worksheet.write('B1', 'Company Name', bold)
    worksheet.write('C1', 'Rating', bold)
    worksheet.write('D1', 'HeadQuater', bold)
    worksheet.write('E1', 'CEO', bold)
    worksheet.write('F1', 'CEO Approval', bold)

    counter = 0
    while (counter < 5):
        url_to_parse = url_list[counter]
        counter = counter + 1
        parse(url_to_parse, minimum)

    print "-"*20
    print "Total number of results returned : %d" % (counter)
    print "-"*20
    workbook.close()

def parse(url_to_parse, minimum):
    global url_list, worksheet
    r = requests.get(url_to_parse)                                                           
    soup = BeautifulSoup(r.content)
    next_links = soup.find_all('li', {"class": "page notranslate"})
    for nl in next_links:
        a = nl.find('a')['href']
        nl = site_name + a
        if nl not in url_list:
            url_list.append(nl)

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

            worksheet.write(counter, 0, counter)
            worksheet.write(counter, 1, Companies[i].text)
            
            
            try:
                worksheet.write(counter, 2, Ratings[i].text)
            except:
                worksheet.write(counter, 2, "unknown")

            try:
                worksheet.write(counter, 3, HeadQuaters[i].find("span", {"class" : "value i-loc"}).text)
            except:
                worksheet.write(counter, 3, "unkown")
            
            try:
                worksheet.write(counter, 4, CEOs[i].find("span", {"class":"fn notranslate"}).text)
            except:
                worksheet.write(counter, 4, "unknown")

            try:
                worksheet.write(counter, 5, CEOs[i].find("span", {"class": "approvalPercent"}).text[:-1])
            except:
                worksheet.write(counter, 5, "0")

                                     

def main():
    url = "http://www.glassdoor.com/Reviews/information-technology-reviews-SRCH_II10013.0,22.htm"
    minimum = input("What is the minimum rating of the companies you are searching for:")
    begin_parsing(url, minimum)

#http://www.glassdoor.com/Reviews/information-technology-company-reviews-SRCH_II10013.0,22_IP3.htm

main()
