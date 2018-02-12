import sqlite3
conn = sqlite3.connect("Reports.db")
c = conn.cursor()



def create_table(cursor, table_name: str, columns: list):
    sql_columns = ", ".join(columns)
    request = "CREATE TABLE IF NOT EXISTS {}({})".format(table_name, sql_columns)
    cursor.execute(request)

def add_data(cursor, table, data: dict):
    data = {key: str(data[key]) for key in data}
    columns = list(data.keys())
    values = [data[column] for column in columns]
    sql_columns = "'" + "','".join(columns) + "'"
    sql_values = "'" + "','".join(values) + "'"
    request = "INSERT INTO {}({}) VALUES ({})".format(table, sql_columns, sql_values)
    cursor.execute(request)
    cursor.connection.commit()


start_request = """ 
CREATE TABLE IF NOT EXISTS Doctors (
	first_name	TEXT,
	middle_name	TEXT,
	second_name	TEXT
);
CREATE TABLE IF NOT EXISTS Medicine (
	name TEXT
);
CREATE TABLE IF NOT EXISTS Reports (
	date	INTEGER,
	doctor_id	INTEGER NOT NULL,
	diagnosis	TEXT,
	medicine_id	INTEGER,
	position_of_electrodes	TEXT,
	comments	TEXT,
	FOREIGN KEY (doctor_id) REFERENCES Doctors(_rowid_),
	FOREIGN KEY (medicine_id) REFERENCES Medicine(_rowid_)
);
"""


# doctor_data = {"first_name" : "Игорь", "middle_name": "Вячеславович", "second_name" : "Костецкий"}
# add_data(c, "Doctors", doctor_data)

medicine_data = {"name": "ketamine"}
add_data(c, "Medicine", medicine_data)

# report_data = {"Date":1, "Doctor_id": 2, "Diagnosis": "abba", "Drug": 1,
#                "Position_of_electrodes": "here", "Comments": "All your base are belong to us"}
# add_data(c, "Reports", report_data)
c.connection.commit()