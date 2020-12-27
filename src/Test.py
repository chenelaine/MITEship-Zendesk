
#
#Created on December 19, 2020
#@author: Elaine Chen
#
#This is a sandbox
#

import os
import datetime
import requests
import copy
import csv

print('*****      *** ')
print('*         *   *')
print('*****     *')
print('*         *   *')
print('***** *    ***   *')




'''
#Welcome message
print('********************************************************************')
print('This is a sandbox for learning python.')
print('Press any key to continue:')
print('********************************************************************')
input()

#**************** Nullify agent username and pw for security
agentUsername = 'null'
agentPassword = 'null'

#**************** Getting Zendesk agent login credentials from the user
agentUsername = input('Please enter Zendesk agent username:')
agentPassword = input('Please enter Zendesk agent password:')

# Compiling credentials
credentials = agentUsername, agentPassword

#**************** Getting ready to pull down the backup
#set up session variable
session = requests.Session()
session.auth = credentials

#set up zendesk url, language
zendesk = 'https://tuftsecenter.zendesk.com'
locale = 'en-US'

#pull down date, compile backup path, mkdir if not present
date = datetime.date.today()
backup_path = os.path.join(str(date), locale)
if not os.path.exists(backup_path):
    os.makedirs(backup_path)
  
#set up the log
log = []
    

#Try to make a category
headers = {
    'Content-Type': 'application/json',
}

data = '{"category": {"position": 2, "locale": "en-us", "name": "Super Hero Tricks", "description": "This category contains a collection of super hero tricks"}}'


response = requests.post('https://tuftsecenter.zendesk.com/api/v2/help_center/categories.json', headers, data, auth=(credentials))

https://tuftsecenter.zendesk.com/api/v2/help_center/categories.json \
  -d '{"category": {"position": 1, "locale": "en-us", "name":  "Super Hero Tricks",\
  "description": "This category contains a collection of super hero tricks"}}' \
  -v -u agentUsername:agentPassword -X -POST -H "Content-Type: application/json"
'''

