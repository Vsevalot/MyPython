# -*- coding: utf-8 -*-
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta
import random


def generate_dataset(dataSource):
    print("Visit https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets "
          "to learn how to create your own datasets.")

    minStartTimeNs = str(int((datetime.now() + timedelta(hours=-1)).timestamp()*1000000000)) # unix time in ns
    maxEndTimeNs = str(int((datetime.now() + timedelta(hours=1)).timestamp()*1000000000)) # unix time in ns

    # Add 10 data points
    points = []
    data_formats = [field["format"] for field in dataSource["dataType"]["field"]]
    for i in range(10): # generate random values for now each 5 minutes after the moment
        startTimeNanos = str(int((datetime.now() + timedelta(minutes=5*i)).timestamp()*1000000000)) # unix time in ns
        endTimeNanos = startTimeNanos
        value = []
        for field in data_formats:
            if field == "integer":
                value.append({"intVal" : str(random.randint(-1000, 1000))})
            if field == "floatPoint":
                value.append({"fpVal" : str(round(random.uniform(-1000, 1000), 5))})
            if field == "string":
                random_chars = [chr(random.randint(65, 90)) for i in range(10)]
                value.append({"stringVal" : ''.join(random_chars)})

        point = {
            "startTimeNanos": startTimeNanos,
            "endTimeNanos": endTimeNanos,
            "dataTypeName": dataSource["dataType"]["name"],
            "value": value
        }
        points.append(point)

    dataset = {
        "minStartTimeNs": minStartTimeNs,
        "maxEndTimeNs": maxEndTimeNs,
        "dataSourceId":dataSource["dataStreamId"],
        "point": points
        }

    return dataset


if __name__ == "__main__":
    # Create a flow
    path_to_secret = "client_secret.json"  # Set path to your client_secret.json here
    scopes = ["email profile",
              'https://www.googleapis.com/auth/fitness.activity.read',
              'https://www.googleapis.com/auth/fitness.activity.write',
              'https://www.googleapis.com/auth/fitness.body.read',
              'https://www.googleapis.com/auth/fitness.body.write']

    flow = InstalledAppFlow.from_client_secrets_file(path_to_secret, scopes=scopes)

    # Confirm credentials
    credentials = flow.run_local_server(host='localhost',
                                        port=8080,
                                        authorization_prompt_message='If your browser haven\'t opened, '
                                                                     'please visit this URL: {url}',
                                        success_message='The auth authorization is complete. You may close this tab.',
                                        open_browser=True)
    # Activate fitness service
    fit_service = build('fitness', 'v1', credentials=credentials)

    # Work with an user
    fit_users = fit_service.users()

    # Take a list of existing dataSources
    dataSources = fit_users.dataSources().list(userId='me').execute()['dataSource']

    # Generate list of datasets
    datasets = [generate_dataset(dataSource) for dataSource in dataSources]

    # Save each dataset to json and patch to appropriate dataSource
    for i in range(len(datasets)):
        fit_users.dataSources().datasets().patch(userId='me',
                                                 dataSourceId=datasets[i]['dataSourceId'],
                                                 datasetId="{}-{}".format(datasets[i]["minStartTimeNs"],
                                                                          datasets[i]["maxEndTimeNs"]),
                                                 body=datasets[i]).execute()

        f = open("{}_dataset.json".format(dataSources[i]["name"]), 'w')  # save your dataset to json
        json.dump(datasets[i], f, sort_keys=True, indent=4)
        f.close()
        print("Dataset has been successfully created, patched to google fit, and saved to a json file.")


    # Get datapoints from appropriate dataSource
    for i in range(len(datasets)):
        datasetId = "{}-{}".format(datasets[i]["minStartTimeNs"],  # A period of time we're interested in
                                   datasets[i]["maxEndTimeNs"])

        # Use "get" method to read dataset values from a dataSource
        get_request = fit_users.dataSources().datasets().get(userId='me',
                                                             dataSourceId=dataSources[i]["dataStreamId"],
                                                             datasetId=datasetId).execute()

        f = open("got_{}_datapoints.json".format(dataSources[i]["name"]), 'w')  # save your dataset to json
        json.dump(get_request, f, sort_keys=True, indent=4)
        f.close()

        beginning = datetime.fromtimestamp(int(datasetId.split('-')[0][:-9]))
        end = datetime.fromtimestamp(int(datasetId.split('-')[-1][:-9]))
        print("Datapoints from {} to {} have been saved to a json file.".format(beginning, end))

    print("Complete.")
    print("Read got json files and get new datapoints in your own of time")