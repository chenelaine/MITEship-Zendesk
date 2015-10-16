'''
Created on Oct 16, 2015

@author: Elaine
'''
from setuptools.package_index import Credential

''' **************** WELCOME  '''
print('Welcome to the MIT Trust Center Zendesk knowledgebase backup script.')
print('Press any key to continue...')
input()

''' **************** Setting up date and time '''
import os
import datetime
import requests
import csv

''' **************** Getting Zendesk agent login credentials from the user'''
agentUsername = input('Please enter Zendesk agent username:')
agentPassword = input('Please enter Zendesk agent password:')

''' Compiling credentials'''
credentials = agentUsername, agentPassword

''' **************** Getting ready to pull down the backup'''

session = requests.Session()
session.auth = credentials

zendesk = 'https://miteship.zendesk.com'
language = 'en-US'

date = datetime.date.today()
backup_path = os.path.join(str(date), language)
if not os.path.exists(backup_path):
  os.makedirs(backup_path)
  
endpoint = zendesk + '/api/v2/help_center/en-us/articles.json'.format(locale=language.lower()) 

print('Press any key to continue...')
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
     for article in data['articles']:
         title = '<h1>' + article['title'] + '</h1>'
         filename = '{id}.html'.format(id=article['id'])
         with open(os.path.join(backup_path, filename), mode='w', encoding='utf-8') as f:
             f.write(title + '\n' + article['body'])
         '''articleRawTitle = '{title} copied!'.format(title=article['title'])
         print(artileRawTitle.encode('cp850', errors='replace'))'''
         articleCount = articleCount + 1
         print('Article #', articleCount, 'written to file')
     
     '''page through the results until next page is null'''
     endpoint = data['next_page']  


'''
'C:\CLOUDROOT\Dropbox (MIT)\MIT Stuff\TRUSTCENTERSTUFF\elaine-sandbox\zendesk-backup
'''
     
     
