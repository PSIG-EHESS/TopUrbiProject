import pandas as pd
import pyodbc

def read_csv_to_dataframe(csv_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    print("CSV Headers:", df.columns.tolist())  # Print headers for debugging
    print("First few rows of the CSV:\n", df.head())  # Print first few rows for debugging
    return df

def update_access_table_from_csv(csv_path, access_db_path, table_name, key_field, update_fields):
    # Read the CSV file into a DataFrame
    df = read_csv_to_dataframe(csv_path)

    # Build the connection string to the Access database
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
        r'DBQ=' + access_db_path + ';'
    )
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Check if key_field and update_fields exist in the DataFrame
    if key_field not in df.columns:
        print(f"Key field '{key_field}' not found in CSV headers.")
        return
    for field in update_fields:
        if field not in df.columns:
            print(f"Update field '{field}' not found in CSV headers.")
            return

    # Iterate over the DataFrame rows and update the Access table
    for index, row in df.iterrows():
        try:
            entry_id = row[key_field]
            province_value = row[update_fields[0]]
            region_value = row[update_fields[1]]

            # Construct the conditional SQL statement
            update_sql = f"""
            UPDATE {table_name}
            SET Province = ?, region = ?
            WHERE {key_field} = ?
            AND (
                (majortype = 'settlement')
                OR
                (majortype = 'human_group' AND conf_loc <> 0 AND conf_loc <> 5)
            )
            """
            cursor.execute(update_sql, province_value, region_value, entry_id)
        except Exception as e:
            print(f"Error updating row with {key_field}={entry_id}: {e}")

    conn.commit()
    conn.close()

# Parameters
csv_path = r"D:\EHESS\Workbench\processing\Input\alcedo_structured_provinces_generic.csv"
access_db_path = r"D:\EHESS\TopUrbi_2024.accdb"
table_name = "alcedo_structured"
key_field = "entry_id"
update_fields = ["province_gener", "region_gener"]

# Update the Access table
update_access_table_from_csv(csv_path, access_db_path, table_name, key_field, update_fields)
