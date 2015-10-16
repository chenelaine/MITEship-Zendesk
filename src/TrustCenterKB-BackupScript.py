'''
Created on Oct 16, 2015

@author: Elaine
'''
from setuptools.package_index import Credential

''' **************** WELCOME  '''
print('********************************************************************')
print('Welcome to the MIT Trust Center Zendesk knowledgebase backup script.')
print('********************************************************************')
print('Press any key to continue...')
input()

''' **************** Setting up date and time '''
import os
import datetime
import requests
import csv

''' **************** Nullify agent username and pw for security ''' 
agentUsername = 'null'


''' **************** Getting Zendesk agent login credentials from the user'''
agentUsername = input('Please enter Zendesk agent username:')
agentPassword = input('Please enter Zendesk agent password:')

''' Compiling credentials'''
credentials = agentUsername, agentPassword

''' **************** Getting ready to pull down the backup'''
''' set up session variable'''
session = requests.Session()
session.auth = credentials

'''set up zendesk url, language'''
zendesk = 'https://miteship.zendesk.com'
language = 'en-US'

'''pull down date, compile backup path, mkdir if not present'''
date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
  os.makedirs(backup_path)
  
''' set up the log'''
log = []
    
''' set up the endpoint, this is what is actually used to pull down the content'''  
endpoint = zendesk + '/api/v2/help_center/en-us/articles.json'.format(locale=language.lower()) + '?include=users,sections,categories'

print('Press any key to start the backup. This will take a few moments.')
input()

''' **************** Posting the actual request for backup'''
response = session.get(endpoint)

'''Page through all the articles and keep retrieving until there are no more pages'''
articleCount = 0
while endpoint:
    
     '''get the endpoint in json format'''
     response = session.get(endpoint)
     
     '''exit if error'''
     if response.status_code != 200:
         print('Failed to retrieve articles with error {}'.format(response.status_code))
         exit()
         
     '''Format result into a Python dictionary '''
     data = response.json()

     '''Print article titles for reference'''
     sectionID = 0
     articleID = 0
     categoryID = 0
     
     '''Iterate through articles'''
     for article in data['articles']:
         
         ''' Get category and section ID and title '''
         sectionName = 'null'
         categoryName = 'null'
         for section in data['sections']:
             if ( section['id'] == article['section_id'] ):
                sectionName = section['name']
                for category in data['categories']:
                     if ( category['id'] == section['category_id']):
                          categoryName = category['name']
          
         articleName = article['title']
         categoryTitle = '<h1>' + categoryName + '</h1>\n'                
         sectionTitle = '<h2>' + sectionName + '</h2>\n'         
         articleTitle = '<h3>' + articleName + '</h3>\n'
         articleFilename = '{id}.html'.format(id=article['id'])
             
         with open(os.path.join(backup_path, articleFilename), mode='w', encoding='utf-8') as f:
             f.write(categoryTitle + '\n' + sectionTitle + '\n' + articleTitle + '\n' + article['body'])
         
         ''' this was giving the script trouble bc command cannot display non
             unicode characters. comment out for now until we figure out how to 
             reformat those pesky special characters. '''
         '''articleRawTitle = '{title} copied!'.format(title=article['title'])
         print(artileRawTitle.encode('cp850', errors='replace'))'''
         
         ''' count how many articles we wrote to file'''
         articleCount = articleCount + 1
         print('Article #', articleCount, 'written to file')
         log.append((articleFilename, categoryName, sectionName, articleName))
     
     '''page through the results until next page is null'''
     endpoint = data['next_page']  

''' Write log to CSV'''
with open(os.path.join(backup_path, '_log.csv'), mode='wt', encoding='utf-8') as f:
     writer = csv.writer(f)
     writer.writerow( ('File', 'Category', 'Section', 'Title') )
     for article in log:
         writer.writerow(article)

     
     
