
def add_data(table, data: dict):
    data = {key: str(data[key]) for key in data}
    columns = list(data.keys())
    values = [data[column] for column in columns]
    sql_columns = "'" + "','".join(columns) + "'"
    sql_values = "'" + "','".join(values) + "'"
    request = "INSERT INTO {}({}) VALUES ({})".format(table, sql_columns, sql_values)
    return request


report_data = {"Record_id":1, "Date":1, "Doctor_id": 2, "Diagnosis": "abba", "Drug": "sad",
               "Position_of_electrodes": "here", "Comments": "All your base are belong to us"}

print(add_data("Reports", report_data))