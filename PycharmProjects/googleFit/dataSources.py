# -*- coding: utf-8 -*-
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import lab_settings as lab

def generate_source(data_source=''):
    print("Visit https://developers.google.com/fit/rest/v1/reference/users/dataSources to learn how to create "
          "your own data source.")
    if data_source[-4:] == 'json':
        return json.load(open(data_source, 'r'))
    elif data_source == "accelerometer":
        return lab.data_source_accelerometer
    elif data_source == "power":
        return lab.data_source_power
    else:
        print('Set a path to a dataSource json file or set the argument for generate_source() to "accelerometer" or '
              '"power" to use default lab data sources')
        exit(0)

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

    # Work with an user
    fit_users = fit_service.users()

    # Create your own data sources
    # Make a request to create a dataSource. Argument body expects dict of your dataSource
    accelerometer_source = fit_users.dataSources().create(userId='me', body=generate_source("accelerometer")).execute()

    # accelerometer_source is the same json as given dataSource with an additional field 'dataStreamId'
    f = open('accelerometer_source.json', 'w') # save your new dataSource to json
    json.dump(accelerometer_source, f, sort_keys=True, indent=4)
    f.close()

    # Make a request to create a dataSource. Argument body expects dict of your dataSource
    power_source = fit_users.dataSources().create(userId='me', body=generate_source("power")).execute()

    # power_source is the same json as given dataSource with an additional field 'dataStreamId'
    f = open("power_source.json", 'w') # save your new dataSource to json
    json.dump(power_source, f, sort_keys=True, indent=4)
    f.close()

    # You can call a list of existing dataSources
    dataSources_list = (fit_users.dataSources().list(userId='me').execute())['dataSource']

    print('')
    for source in dataSources_list:
        print("Created dataSource, name : {}".format(source["name"]))

    # You can delete dataSource by dataStreamId
    sourceID = ''
    if sourceID != '':
        fit_users.dataSources().delete(userId='me', dataSourceId=sourceID).execute()

    print("\nFinished. You've successfully created accelerometer and eeg power data sources.")
    print("Read your json dataSource files, and if everything is clear, run the datasets.py script")