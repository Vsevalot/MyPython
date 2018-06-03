# -*- coding: utf-8 -*-
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta

import lab_settings as lab



CLEAR_START = True # Set True if you want to start the lab from the beginning

"""
This script creates two data sources for your google fit project: accelerometer and eeg.
Make sure to put client_secret.json file in the work directory or set path in the "path_to_secret"
If you want to change any google fit value, change it in lab_settings.py
"""

def create_acce_source():
    data_source_acce = {
        "name": "accelerometer",
        "dataStreamName": lab.accelerometer_stream_name,
        "type": "raw",
        "application": {
            "name": lab.application_name,
            "version": "1"
        },
        "dataType": {
            "name": "accelerometer data",
            "field": [
                {
                    "name": "ax",
                    "format": lab.accelerometer_data_format
                },
                {
                    "name": "ay",
                    "format": lab.accelerometer_data_format
                },
                {
                    "name": "az",
                    "format": lab.accelerometer_data_format
                }
            ]
        }
    }
    fit_users.dataSources().create(userId='me', body=data_source_acce).execute()

def create_eeg_source():
    data_source_eeg = {
        "dataStreamName": lab.eeg_stream_name,
        "name": "band power",
        "type": "raw",
        "application": {
            "name": lab.application_name,
            "version": "1"
        },
        "dataType": {
            "name": "eeg band power",
            "field": [
                {
                    "name": "theta",
                    "format": lab.eeg_data_format
                },
                {
                    "name": "alpha",
                    "format": lab.eeg_data_format
                },
                {
                    "name": "betal",
                    "format": lab.eeg_data_format
                },
                {
                    "name": "betah",
                    "format": lab.eeg_data_format
                }
            ]
        }
    }
    fit_users.dataSources().create(userId='me', body=data_source_eeg).execute()

def create_eeg_datapoint(dataSourceId, dataTypeName):
    if lab.eeg_data_format == "integer":
        format = "intVal"
    elif lab.eeg_data_format == "float":
        format = "fpVal"
    else:
        format = "unknown"
        print("Unknown data format")
        exit(33)

    minStartTimeNs = str(int((datetime.now() + timedelta(hours=-1)).timestamp()*1000000000))
    maxEndTimeNs = str(int((datetime.now() + timedelta(hours=1)).timestamp()*1000000000))
    startTimeNanos = str(int(datetime.now().timestamp()*1000000000))
    endTimeNanos = startTimeNanos
    data_point = {
        "minStartTimeNs": minStartTimeNs,
        "maxEndTimeNs": maxEndTimeNs,
        "dataSourceId":dataSourceId,
        "point": [
            {
                "startTimeNanos": startTimeNanos,
                "endTimeNanos": endTimeNanos,
                "dataTypeName": dataTypeName,
                "value": [
                    {format: '1'},
                    {format: '2'},
                    {format: '3'},
                    {format: '4'}
                    ]
                }
            ]
        }
    return data_point

def create_acce_datapoint(dataSourceId, dataTypeName):
    if lab.accelerometer_data_format == "integer":
        format = "intVal"
    elif lab.accelerometer_data_format == "float":
        format = "fpVal"
    else:
        format = "unknown"
        print("Unknown data format")
        exit(33)

    minStartTimeNs = str(int((datetime.now() + timedelta(hours=-1)).timestamp()*1000000000))
    maxEndTimeNs = str(int((datetime.now() + timedelta(hours=1)).timestamp()*1000000000))
    startTimeNanos = str(int(datetime.now().timestamp()*1000000000))
    endTimeNanos = startTimeNanos
    data_point = {
        "minStartTimeNs": minStartTimeNs,
        "maxEndTimeNs": maxEndTimeNs,
        "dataSourceId":dataSourceId,
        "point": [
            {
                "startTimeNanos": startTimeNanos,
                "endTimeNanos": endTimeNanos,
                "dataTypeName": dataTypeName,
                "value": [
                    {format: '97'},
                    {format: '98'},
                    {format: '99'}
                    ]
                }
            ]
        }
    return data_point

if __name__ == "__main__":
    # Create a flow
    path_to_secret = "client_secret.json"
    flow = InstalledAppFlow.from_client_secrets_file(
        path_to_secret,
        scopes=["email profile",
                'https://www.googleapis.com/auth/fitness.activity.read',
                'https://www.googleapis.com/auth/fitness.activity.write',
                'https://www.googleapis.com/auth/fitness.body.read',
                'https://www.googleapis.com/auth/fitness.body.write'
                ])

    # Confirm credentials
    credentials = flow.run_local_server(host='localhost',
                                        port=8080,
                                        authorization_prompt_message='Please visit this URL: {url}',
                                        success_message='The auth flow is complete; you may close this window.',
                                        open_browser=True)
    fit_service = build('fitness', 'v1', credentials=credentials)
    fit_users = fit_service.users()
    fit_dataSources = fit_users.dataSources()
    request = fit_dataSources.list(userId='me')
    dataSources_list = (request.execute())['dataSource']

    if CLEAR_START: # Delete all previous data sources
        for sourceId in dataSources_list:
            fit_dataSources.delete(userId='me', dataSourceId=sourceId['dataStreamId'])

    if dataSources_list == []: # If there is no data sources in the project
        # Create your own data sources
        create_acce_source() # accelerometer
        create_eeg_source() # eeg
        dataSources_list = (request.execute())['dataSource']

    dataSources_dict = {source['name']: source for source in dataSources_list}


    acce_data_point = create_acce_datapoint(dataSources_dict["accelerometer"]["dataStreamId"],
                                            dataSources_dict["accelerometer"]["dataType"])

    eeg_data_point = create_eeg_datapoint(dataSources_dict["eeg"]["dataStreamId"],
                                            dataSources_dict["eeg"]["dataType"])

    acce_request = fit_dataSources.datasets().patch(userId='me',
                                                    dataSourceId=acce_data_point['dataSourceId'],
                                                    datasetId="{}-{}".format(acce_data_point["minStartTimeNs"],
                                                                             acce_data_point["maxEndTimeNs"]),
                                                    body=acce_data_point).execute()

    eeg_request = fit_dataSources.datasets().patch(userId='me',
                                                    dataSourceId=eeg_data_point['dataSourceId'],
                                                    datasetId="{}-{}".format(eeg_data_point["minStartTimeNs"],
                                                                             eeg_data_point["maxEndTimeNs"]),
                                                    body=eeg_data_point).execute()

    datasetId = "1527996882233987072-1528004082233987072"
    request = fit_dataSources.datasets().get(userId='me',
                                             dataSourceId=dataSources_dict["accelerometer"]["dataStreamId"],
                                             datasetId=datasetId).execute()
    print(1)