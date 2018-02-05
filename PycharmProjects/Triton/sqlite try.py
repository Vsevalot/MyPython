import sqlite3
conn = sqlite3.connect("Reports.db")
c = conn.cursor()



def create_table(cursor, table_name: str, columns: list):
    sql_columns = ", ".join(columns)
    request = "CREATE TABLE IF NOT EXISTS {}({})".format(table_name, sql_columns)
    cursor.execute(request)

def add_data(cursor, table, data):
    sql_data = ", ".join(data)
    request = "INSERT INTO {} VALUES ({})".format(table, sql_data)
    cursor.execute(request)
    cursor.connection.commit()

doctor_columns = ["First_name TEXT", "Middle_name TEXT", "Second_name TEXT PRIMARY KEY"]

reports_columns = ["Record TEXT PRIMARY KEY", "Doctor TEXT FOREIGN KEY(Doctors) REFERENCES Doctors(Second_name)",
                   "Operation TEXT DEFAULT VALUE 'Unknown'", "Drugs TEXT", ""]



create_table(c, "Doctors", doctor_columns)

doctor_data = ["'Иван'", "'Иванов'", "'Багин'"]
add_data(c, "Doctors", doctor_data)