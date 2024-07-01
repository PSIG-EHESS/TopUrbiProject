import pyodbc
import pandas as pd

def import_csv_to_access(csv_path, access_db_path, table_name):
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + access_db_path + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    
    # Drop the table if it exists
    try:
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
    except pyodbc.Error as ex:
        print(f"An error occurred while dropping the table: {ex}")
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path, sep=';')
    columns = df.columns
    
    # Determine column types
    column_types = []
    for col in columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            column_types.append(f"[{col}] DOUBLE")
        else:
            column_types.append(f"[{col}] TEXT")
    
    # Create table statement
    create_table_sql = f"CREATE TABLE {table_name} ({', '.join(column_types)})"
    cursor.execute(create_table_sql)
    
    # Replace NaN with None for SQL insertion
    df = df.where(pd.notnull(df), None)
    
    # Insert data into the table
    for row in df.itertuples(index=False, name=None):
        cursor.execute(f"INSERT INTO {table_name} VALUES ({','.join(['?' for _ in columns])})", row)
    conn.commit()
    conn.close()

# Parameters
csv_path = r"F:\EHESS\Workbench\processing\Output\Alcedo_geo.csv"
access_db_path = r"F:\EHESS\TopUrbi_2024.accdb"
table_name = "Alcedo_geo"

# Import CSV into Access
import_csv_to_access(csv_path, access_db_path, table_name)
