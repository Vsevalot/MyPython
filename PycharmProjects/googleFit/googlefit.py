# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 16:27:18 2017

@author: a.m.syskov
"""
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta
import calendar

def date_to_nano(ts):
    """
    Takes a datetime object and returns POSIX UTC in nanoseconds
    """
    return calendar.timegm(ts.utctimetuple()) * int(1e9)

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/fitness.activity.read', 'https://www.googleapis.com/auth/fitness.activity.write'])

credentials = flow.run_local_server(host='localhost',
    port=8080, 
    authorization_prompt_message='Please visit this URL: {url}', 
    success_message='The auth flow is complete; you may close this window.',
    open_browser=True)

fit_service = build('fitness', 'v1', credentials=credentials)
fit_users = fit_service.users()


fit_dataSources = fit_users.dataSources()
request = fit_dataSources.list(userId='me')
dataSources_list = []
dataSources_list = (request.execute())['dataSource']

#request = fit_dataSources.delete(userId='me', dataSourceId='derived:com.bioeng.eeg.freqband:221383075641:Example Manufacturer:ExampleTablet:1000001:EEG freq band data')
#request.execute()

#for itemDS in dataSources_list:
#    request = fit_dataSources.delete(userId='me', dataSourceId=itemDS['dataStreamId']) 
#    try:
#        request.execute()
#    except:
#        print(itemDS['dataStreamId'])

#fp = open('datasource.json', 'r')
#jsonbody = json.load(fp)
#fp.close()
#request = fit_users.dataSources().create(userId='me', body=jsonbody)
#request.execute()

#datasetId = '1509614305000000000-1509621505000000000'
#dataSourceId = 'derived:com.bioeng.eeg.freqband:221383075641:Example Manufacturer:ExampleTablet:1000001:EEG freq band data'
#request = fit_dataSources.datasets().get(userId='me', dataSourceId=dataSourceId, datasetId=datasetId)
#point_list = []
#point_list = (request.execute())['point']

minStartTimeNs =  date_to_nano(datetime.now() + timedelta(hours=-1))
maxEndTimeNs =  date_to_nano(datetime.now() + timedelta(hours=1))
startTimeNanos = date_to_nano(datetime.now())
endTimeNanos = startTimeNanos
body_dict = {}

fp = open('datapoint.json', 'r')
body_dict = json.load(fp)
fp.close()

body_dict['minStartTimeNs'] = minStartTimeNs
body_dict['maxEndTimeNs'] = maxEndTimeNs
point_list = []
point_list = body_dict['point']
for itemPoint in point_list:
    itemPoint['startTimeNanos'] = startTimeNanos
    itemPoint['endTimeNanos'] = endTimeNanos

datasetId = '{minStartTimeNs_}-{maxEndTimeNs_}'.format(minStartTimeNs_=minStartTimeNs,maxEndTimeNs_=maxEndTimeNs)
request = fit_dataSources.datasets().patch(userId='me', dataSourceId=body_dict['dataSourceId'], datasetId=datasetId, body=body_dict)
obj_dict = {}
obj_dict = request.execute()

print(obj_dict)

#print json.dumps(dataSources_dict, sort_keys=True, indent=4)

  
