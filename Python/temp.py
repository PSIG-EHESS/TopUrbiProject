import pyodbc
import pandas as pd

def export_access_to_csv(access_db_path, table_name, csv_path, integer_columns, double_columns):
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
    
    # Ensure integer columns remain integers
    for col in integer_columns:
        df[col] = df[col].astype('Int64')  # Int64 allows for nullable integers
    
    # Convert double columns to strings with comma as decimal delimiter
    for col in double_columns:
        df[col] = df[col].apply(lambda x: f"{x:.6f}".replace('.', ',') if pd.notnull(x) else '')
    
    df.to_csv(csv_path, sep='\t', index=False, encoding='utf-8')
    conn.close()

# Parameters
access_db_path = r"D:\EHESS\TopUrbi_2024.accdb"
table_name = "Alcedo_structured"
csv_path = r"D:\EHESS\Workbench\processing\Input\Alcedo_structured.csv"
gdb_path = r"D:\EHESS\Workbench\Geodata\Alcedo.gdb"
featureclass_name = "Alcedo_Places_from_Access"
x_col = "Lon"
y_col = "Lat"

# Integer and double column names
integer_columns = ["Featuretype_AAT", "conf_loc", "featuretype_literal_AAT"]
double_columns = ["Lon", "Lat"]  # Add more double columns if needed

# Export Access table to CSV
export_access_to_csv(access_db_path, table_name, csv_path, integer_columns, double_columns)
