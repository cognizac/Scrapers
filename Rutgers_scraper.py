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

def main():
    schools = ['ais','finance-economics','mgb','msis','marketing','scmms']

    br = mechanize.Browser()

    contacts = []

    for school in schools:
        print "Opening " + school + '...'
        br.open('http://business.rutgers.edu/'+ school + '/faculty')
        soup = BeautifulSoup(br.response().read())

        people = soup.find(attrs={'class':'view-content'}).findAll(attrs={'class':'field-content'})
        for person in people:
            thiscontact = []
            thiscontact.append(' '.join(person.findAll('a')[1].text.split()))
            info = person.findAll('br')
            thiscontact.append(unicode(info[0].nextSibling.text))
            thiscontact.append(' '.join(info[1].nextSibling.split()))
            if info[2].nextSibling:
                thiscontact.append(unicode(info[2].nextSibling.text))
            else:
                thiscontact.append("N/A")

            contacts.append(thiscontact)

    fileout = open('Rutgers_contacts.tsv','w')
    fileout.write('Name\tTitle\tArea\tContact\n')
    for contact in contacts:
        fileout.write(str(contact[0])+'\t'+str(contact[1])+'\t'+str(contact[2])+'\t'+str(contact[3])+'\n')
    fileout.close()
if __name__ == '__main__':
    main()
