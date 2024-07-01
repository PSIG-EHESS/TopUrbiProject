##Export Alcedo_sructured table in MS Access into a csv

import pyodbc
import pandas as pd

def export_access_to_csv(access_db_path, table_name, csv_path):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + access_db_path + ';'
    )
    try:
        conn = pyodbc.connect(conn_str)
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        if sqlstate == 'IM002':
            print("ODBC Driver not found. Ensure that the Microsoft Access ODBC driver is installed.")
        else:
            print(f"An error occurred: {ex}")
        return
    
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    df.to_csv(csv_path, sep=';', index=False, encoding='utf-8')
    conn.close()


# Parameters
access_db_path = r"F:\EHESS\TopUrbi_2024.accdb"
table_name = "Alcedo_structured"
csv_path = r"F:\EHESS\Workbench\processing\Input\Alcedo_structured.csv"
gdb_path = r"F:\EHESS\Workbench\Geodata\Alcedo.gdb"
featureclass_name = "Alcedo_Places_from_Access"
x_col = "Lon"
y_col = "Lat"

# Export Access table to CSV
export_access_to_csv(access_db_path, table_name, csv_path)
