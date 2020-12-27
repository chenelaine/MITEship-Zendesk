#
#Created on Oct 16, 2015
#
#@author: Elaine
#

import os
import datetime
import requests
import copy
import csv



#Welcome message
print('********************************************************************')
print('Welcome to the Zendesk knowledgebase backup script.')
print('Press any key to continue:')
print('********************************************************************')
input()

#**************** set up session variable
session = requests.Session()

#**************** Nullify agent username and pw for security
#agent_username = 'null'

#**************** Getting Zendesk agent login credentials from the user
#agent_username = input('Please enter Zendesk agent username:')
#agent_password = input('Please enter Zendesk agent password:')

# Compiling credentials
#credentials = agent_username, agent_password

#**************** Getting ready to pull down the backup
#session.auth = credentials

#set up zendesk url, language
print('Enter Zendesk name:', end='')
zendeskname = input()
zendesk = 'https://'+ zendeskname + '.zendesk.com'
print('Zendesk URL is', zendesk, '. Is this correct? [y/n]')
url_confirmation = input()
if (url_confirmation.lower() != 'y'):
    print('OK. Goodbye!')
    exit()
    
#pull down date, compile backup path, mkdir if not present
date = datetime.date.today()
backup_path = os.path.join(str(date), zendeskname)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)
  
#set up the log
log = []

#set up the endpoint, this is what is actually used to pull down the content
language = 'en-US'
endpoint = zendesk + '/api/v2/help_center/en-us/articles.json'.format(locale=language.lower()) + '?include=users,sections,categories'

print('Press any key to start the backup. This will take a few moments.')
input()

#**************** Posting the actual request for backup
response = session.get(endpoint)

#Page through all the articles and keep retrieving until there are no more pages
articleCount = 0
while endpoint:
    
    #get the endpoint in json format
    response = session.get(endpoint)
     
    #exit if error
    if response.status_code != 200:
        print('Failed to retrieve articles with error {}'.format(response.status_code))
        exit()
         
    #Format result into a Python dictionary
    data = response.json()
    
    #Print article titles for reference
    sectionID = 0
    articleID = 0
    categoryID = 0
     
    #Iterate through articles
    for article in data['articles']:
         
        # Get category and section ID and title
        section_name = 'null'
        category_name = 'null'
        for section in data['sections']:
            if ( section['id'] == article['section_id'] ):
                section_name = section['name']
                for category in data['categories']:
                    if ( category['id'] == section['category_id']):
                        category_name = category['name']
          
        article_name = article['title']
        category_title = '<em><strong>CATEGORY:</strong> ' + category_name + '</em>'
        section_title = '<em><strong>SECTION:</strong> ' + section_name + '</em>'
        article_title = '<h1>' + article_name + '</h1>'
        article_filename = '{id}.html'.format(id=article['id'])
         
        file_handle = open(os.path.join(backup_path, article_filename), mode='w', encoding='utf-8')
             
        with file_handle as f:
            # FRONT MATTER
            f.write('<!DOCTYPE html>\n')
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('<meta charset="UTF-8"/>')
            f.write('<title>' + article_name + '\n</title>')
            f.write('</head>\n')
            
            # BODY
            f.write('<body>\n')
            f.write(article_title)
            f.write('<br>')
            f.write(category_title)
            f.write('<br>')
            f.write(section_title)
            f.write('<br>')
            f.write(article['body'])
            f.write('</body>\n')
            
            # END HTML
            f.write('</html>\n')

         
        #count how many articles we wrote to file
        articleCount = articleCount + 1
        print('#',articleCount,': ', article_name)

        log.append((article_filename, category_name, section_name, article_name))
     
        #page through the results until next page is null
        endpoint = data['next_page']

# Write log to CSV
with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8', newline='') as f:
    writer = csv.writer(f,dialect='excel')
    writer.writerow( ('File', 'Category', 'Section', 'Title') )
    for article in log:
        writer.writerow(article)

