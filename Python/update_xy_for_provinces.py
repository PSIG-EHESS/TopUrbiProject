import pandas as pd
import pyodbc

def read_csv_to_dataframe(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    print("CSV Headers:", df.columns.tolist())  # Print headers for debugging
    print("First few rows of the CSV:\n", df.head())  # Print first few rows for debugging
    return df

def update_lat_lon_in_access(csv_path, access_db_path, table_name, key_field, lat_field, lon_field):
    # Read the CSV file into a DataFrame
    df = read_csv_to_dataframe(csv_path)

    # Build the connection string to the Access database
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + access_db_path + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Check if key_field, lat_field, and lon_field exist in the DataFrame
    if key_field not in df.columns:
        print(f"Key field '{key_field}' not found in CSV headers.")
        return
    if lat_field not in df.columns:
        print(f"Latitude field '{lat_field}' not found in CSV headers.")
        return
    if lon_field not in df.columns:
        print(f"Longitude field '{lon_field}' not found in CSV headers.")
        return

    # Iterate over the DataFrame rows and update the Access table
    for index, row in df.iterrows():
        try:
            entidad_id = row[key_field]
            lat_value = row[lat_field]
            lon_value = row[lon_field]

            # Construct the gazetteermatch value with prefix
            gazetteermatch_value = f"hgis:{entidad_id}"

            # Construct the SQL statement
            update_sql = f"""
            UPDATE {table_name}
            SET Lat = ?, Lon = ?
            WHERE gazetteermatch = ?
            """
            cursor.execute(update_sql, lat_value, lon_value, gazetteermatch_value)
        except Exception as e:
            print(f"Error updating row with {key_field}={entidad_id}: {e}")

    conn.commit()
    conn.close()

# Parameters
csv_path = r"D:\EHESS\Workbench\processing\Input\provinces_xy.csv"
access_db_path = r"D:\EHESS\TopUrbi_2024.accdb"
table_name = "alcedo_structured"
key_field = "Entidad_ID"
lat_field = "lat"
lon_field = "lon"

# Update the Access table
update_lat_lon_in_access(csv_path, access_db_path, table_name, key_field, lat_field, lon_field)
