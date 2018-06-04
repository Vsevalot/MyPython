application_name = "BCI study application" # your application name

accelerometer_stream_name = "bci_study_accelerometer" # your accelerometer data stream name
accelerometer_data_format = "integer" # accelerometer data format

power_stream_name = "bci_study_power" # your eeg data stream name
power_data_format = "integer" # eeg data format

"""
Visit https://developers.google.com/fit/rest/v1/reference/users/dataSources to learn how to create your own data source.
"""
data_source_accelerometer = {
    "name": "accelerometer",
    "dataStreamName": accelerometer_stream_name,
    "type": "raw",
    "application": {
        "name": application_name,
        "version": "1"
    },
    "dataType": {
        "name": "accelerometer data",
        "field": [
            {
                "name": "ax",
                "format": accelerometer_data_format
            },
            {
                "name": "ay",
                "format": accelerometer_data_format
            },
            {
                "name": "az",
                "format": accelerometer_data_format
            }
        ]
    }
}

data_source_power = {
    "dataStreamName": power_stream_name,
    "name": "band power",
    "type": "raw",
    "application": {
        "name": application_name,
        "version": "1"
    },
    "dataType": {
        "name": "eeg band power",
        "field": [
            {
                "name": "theta",
                "format": power_data_format
            },
            {
                "name": "alpha",
                "format": power_data_format
            },
            {
                "name": "betal",
                "format": power_data_format
            },
            {
                "name": "betah",
                "format": power_data_format
            }
        ]
    }
}

