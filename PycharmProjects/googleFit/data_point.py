# -*- coding: utf-8 -*-
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
from datetime import datetime, timedelta
import lab_settings as lab
import random


def give_dataset(dataSource):
    print("Visit https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets "
          "to learn how to create your own datasets.")

    minStartTimeNs = str(int((datetime.now() + timedelta(minutes=-1)).timestamp()*1000000000))
    maxEndTimeNs = str(int((datetime.now() + timedelta(hours=1)).timestamp()*1000000000))

    # Add 10 data points
    points = []
    data_formats = [field["format"] for field in dataSource["dataType"]["field"]]
    for i in range(10): # generate random values for now each 5 minutes after the moment
        startTimeNanos = str(int((datetime.now() + timedelta(minutes=5*i)).timestamp()*1000000000))
        endTimeNanos = startTimeNanos
        value = []
        for field in data_formats:
            if field == "integer":
                value.append({field : str(random.randint(-1000, 1000))})
            if field == "floatPoint":
                value.append({field : str(round(random.uniform(-1000, 1000), 5))})
            if field == "string":
                random_chars = [chr(random.randint(65, 90)) for i in range(10)]
                value.append({field : ''.join(random_chars)})

        point = {
            "startTimeNanos": startTimeNanos,
            "endTimeNanos": endTimeNanos,
            "dataTypeName": dataSource["dataType"], # dataSource["dataType"]["name"]
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
                                        success_message='The auth authorization is complete. Close this tab.',
                                        open_browser=True)
    # Activate fitness service
    fit_service = build('fitness', 'v1', credentials=credentials)

    # Work with account user
    fit_users = fit_service.users()

    # load an accelerometer dataSource
    path_to_ads = "accelerometer_source.json"
    accelerometer_ds = json.load(open(path_to_ads, 'r'))

    # load a power dataSource
    path_to_pds = "power_source.json"
    power_ds = json.load(open(path_to_pds, 'r'))

    accelerometer_dataset = give_dataset(accelerometer_ds)
    accelerometer_dataset["point"] = accelerometer_dataset["point"][:1]
    f = open("accelerometer_dataset.json", 'w') # save your new dataset to json
    json.dump(accelerometer_dataset, f, sort_keys=True, indent=4)
    f.close()

    accelerometer_dataset = json.load(open("good_acce.json", 'r'))

    # power_dataset = give_dataset(power_ds)
    # f = open("power_dataset.json", 'w') # save your new dataset to json
    # json.dump(power_dataset, f, sort_keys=True, indent=4)
    # f.close()

    # Use patch method to add a dataset to a dataSource
    fit_users.dataSources().datasets().patch(userId='me',
                                             dataSourceId=accelerometer_dataset['dataSourceId'],
                                             datasetId="{}-{}".format(accelerometer_dataset["minStartTimeNs"],
                                                                      accelerometer_dataset["maxEndTimeNs"]),
                                             body=accelerometer_dataset).execute()

    # # Use patch method to add a dataset to a dataSource
    # fit_users.dataSources().datasets().patch(userId='me',
    #                                          dataSourceId=power_dataset['dataSourceId'],
    #                                          datasetId="{}-{}".format(power_dataset["minStartTimeNs"],
    #                                                                   power_dataset["maxEndTimeNs"]),
    #                                          body=power_dataset).execute()

    datasetId = "{}-{}".format(accelerometer_dataset["minStartTimeNs"], # A period of time we're interested in
                               accelerometer_dataset["maxEndTimeNs"])

    # Use get method to read dataset values from a dataSource
    accelerometer_get_request = fit_users.dataSources().datasets().get(userId='me',
                                             dataSourceId=accelerometer_ds["dataStreamId"],
                                             datasetId=datasetId).execute()

    print(accelerometer_get_request)

    # power_get_request = fit_users.dataSources().datasets().get(userId='me',
    #                                          dataSourceId=power_ds["dataStreamId"],
    #                                          datasetId=datasetId).execute()
    #
    # print(power_get_request)