# -*- coding: utf-8 -*-
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta

"""
This script deletes all datapoints in all dataSources and deletes all dataSources
"""
if __name__ == "__main__":
    # Create a flow
    path_to_secret = "client_secret.json" # Set path to your client_secret.json here
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
                                        success_message='The auth authorization is complete. Close this tab.',
                                        open_browser=True)
    # Activate fitness service
    fit_service = build('fitness', 'v1', credentials=credentials)

    # Work with an user
    fit_users = fit_service.users()

    fit_dataSources = fit_users.dataSources()
    dataSources_list = (fit_users.dataSources().list(userId='me').execute())['dataSource']

    # This virible
    datasetId = "{}-{}".format(int((datetime.now() + timedelta(weeks=-1)).timestamp() * 1000000000),
                               int((datetime.now() + timedelta(hours=+1)).timestamp() * 1000000000))


    for sourceID in dataSources_list:
        for datapoint in dataSources_list:
            fit_dataSources.datasets().delete(userId='me',
                                             dataSourceId=sourceID['dataStreamId'],
                                             datasetId=datasetId).execute()
        fit_dataSources.delete(userId='me', dataSourceId=sourceID['dataStreamId']).execute()

    print("Complete")