import sqlite3
conn = sqlite3.connect("Reports.db")
c = conn.cursor()



def create_table(cursor, table_name: str, columns: list):
    sql_columns = ", ".join(columns)
    request = "CREATE TABLE IF NOT EXISTS {}({})".format(table_name, sql_columns)
    print(request)
    return
    cursor.execute(request)

def add_data(cursor, table, data):
    sql_data = ", ".join(data)
    request = "INSERT INTO {} VALUES ({})".format(table, sql_data)
    cursor.execute(request)
    cursor.connection.commit()

doctor_columns = ["ID PRIMARY KEY" ,"First_name TEXT", "Middle_name TEXT", "Second_name TEXT"]

reports_columns = ["Record TEXT PRIMARY KEY", "Doctor TEXT FOREIGN KEY(Doctors) REFERENCES Doctors(Second_name)",
                   "Operation TEXT DEFAULT VALUE 'Unknown'", "Drugs TEXT", ""]


report_request = """
CREATE TABLE IF NOT EXISTS Reports (
	Record_id	INTEGER NOT NULL UNIQUE,
	Date	INTEGER,
	Doctor_id	INTEGER NOT NULL,
	Diagnosis	TEXT,
	Drug	TEXT,
	Electords_location	TEXT,
	Comments	TEXT,
	FOREIGN KEY (Doctor_id) REFERENCES Doctors(id)
);
"""
print(report_request)

c.execute(report_request)
c.connection.commit()