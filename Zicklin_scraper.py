#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      cognizac
#
# Created:     14/02/2014
# Copyright:   (c) cognizac 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import mechanize
from bs4 import BeautifulSoup
import pickle

def main():

    contacts = []
    br = mechanize.Browser()
    schools = ['accountancy','cis','economics','law','management','marketing','orqm','realestate','statistics']

    for school in schools:
        print "Opening " + school + " page..."
        URL = 'http://zicklin.baruch.cuny.edu/faculty/'+school+'/full-time-faculty'
        br.open(URL)
        soup = BeautifulSoup(br.response().read())
        people = soup.find(attrs={'id':'parent-fieldname-text'}).findAll('tr')[1:]
        print "Extracting contacts..."
        for person in people:
            info = person.findAll('td')
            thiscontact = []
            if info[0].a:
                thiscontact.append(info[0].a.text.encode('ascii','ignore'))
            else:
                thiscontact.append(info[0].text.encode('ascii','ignore'))
            if info[1].text.find('@') != -1:
                thiscontact.append("""N/A""")
                thiscontact.append(school)
                thiscontact.append(info[1].text.encode('ascii','ignore'))
                thiscontact.append(info[2].text.encode('ascii','ignore'))
            else:
                thiscontact.append(info[1].text.encode('ascii','ignore'))
                thiscontact.append(school)
                thiscontact.append(info[2].text.encode('ascii','ignore'))
                thiscontact.append(info[3].text.encode('ascii','ignore'))
            if info[0].a:
                thiscontact.append(str(info[0].a['href']))
            else:
                thiscontact.append("""N/A""")
            print thiscontact
            contacts.append(thiscontact)

    fileout = open('Ziklin_contacts.tsv','w')
    fileout.write('NAME1\tNAME2\tArea\tEmail\tPhone\tPersonal Page\n')
    for contact in contacts:
        fileout.write(str(contact[0])+'\t'+str(contact[1])+'\t'+str(contact[2])+'\t'+str(contact[3])+'\t'+str(contact[4])+'\t'+str(contact[5])+'\n')
    fileout.close()

if __name__ == '__main__':
    main()
