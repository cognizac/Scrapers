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
    br = mechanize.Browser()
    br.open('http://weatherhead.case.edu/faculty/directory?sortBy=p')
    columns = BeautifulSoup(br.response().read()).findAll(attrs={'class':'span6'})

    contacts = []

    for column in columns:
        people = column.findAll('strong')
        info = column.findAll('br')

        for index,person in enumerate(people):
            thiscontact = []
            thiscontact.append(person.text)
            thisinfo = info[index*3].nextSibling.split(',')
            thiscontact.append(thisinfo[0])
            thiscontact.append(thisinfo[1].encode('ascii','ignore'))
            if person.a:
                #print person.a['href']
                br.open('http://weatherhead.case.edu'+str(person.a['href']))
                soup = BeautifulSoup(br.response().read())
                email = soup.find(attrs={'class':'span10'}).a.text
                phone = soup.find(attrs={'class':'span10'}).findAll('br')[2].nextSibling.replace('\t','').replace('\r','').replace('\n','')
                if email:
                    thiscontact.append(email)
                else:
                    thiscontact.append("""N/A""")
                if email:
                    thiscontact.append(phone)
                else:
                    thiscontact.append("""N/A""")
            print thiscontact
            contacts.append(thiscontact)

    fileout = open('CaseWestern_contacts.tsv','w')
    fileout.write('Name\tTitle\tArea\tEmail\tPhone\n')
    for contact in contacts:
        fileout.write(str(contact[0])+'\t'+str(contact[1])+'\t'+str(contact[2])+'\t'+str(contact[3])+'\t'+str(contact[4])+'\n')
    fileout.close()



if __name__ == '__main__':
    main()
