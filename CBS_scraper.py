#-------------------------------------------------------------------------------
# Name:        CBS_scraper.py
# Purpose:     Scrapes the faculty members from Columbia's Business School
#               directory.
#
# Author:      cognizac
#
# Created:     14/02/2014
# Copyright:   (c) cognizac 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from selenium import webdriver
from bs4 import BeautifulSoup
import pickle
import time

def main():
    driver = webdriver.Firefox()
    driver.get('https://www4.gsb.columbia.edu/cbs-directory/faculty-expertise')

    departments = [x for x in driver.find_elements_by_tag_name('option') if x.get_attribute('value')[0]=='7' and x.text!='']

    contacts = []

    for dept in departments:
        dept.click()

    time.sleep(3)
    print "Getting page source..."
    soup = BeautifulSoup(unicode(driver.page_source))
    people = soup.findAll(attrs={'class':'bg'})
    print 'Found ' + str(len(people)) + ' people'
    print people

    for person in people:
        info = person.findAll('a')
        thisperson = []
        thisperson.append(str(info[0].text))
        thisperson.append(str(info[1].text))
        driver.get('https://www4.gsb.columbia.edu/cbs-directory/'+info[0]['href'][info[0]['href'].find('/departments'):])
        thissoup = BeautifulSoup(unicode(driver.page_source))
        thisemail = str(thissoup.find(attrs={'class':'person-coordinates'}).a.text)
        if thisemail:
            thisperson.append(thisemail)
        else:
            thisperson.append("""N/A""")

        print thisperson
        contacts.append(thisperson)
    pickleout = open('contacts','w')
    pickle.dump(contacts,pickleout)
    pickleout.close()
    fileout = open('Contacts_List.csv','w')
    fileout.write('Name\tArea\tContact\n')
    for contact in contacts:
        fileout.write(str(contact[0])+'\t'+str(contact[1])+'\t'+str(contact[2])+'\n')
    fileout.close()

if __name__ == '__main__':
    main()
