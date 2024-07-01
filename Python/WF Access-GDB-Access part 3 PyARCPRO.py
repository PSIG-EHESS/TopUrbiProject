import arcpy
import pandas as pd
import numpy as np

def update_lat_lon_from_geometry(gdb_path, featureclass_name):
    arcpy.env.workspace = gdb_path
    featureclass_path = f"{gdb_path}\\{featureclass_name}"
    
    # Check if Lat and Lon fields exist
    fields = [field.name for field in arcpy.ListFields(featureclass_path)]
    if 'Lat' not in fields or 'Lon' not in fields:
        raise ValueError("The feature class must contain 'Lat' and 'Lon' fields")
    
    with arcpy.da.UpdateCursor(featureclass_path, ['SHAPE@XY', 'Lat', 'Lon']) as cursor:
        for row in cursor:
            x, y = row[0]
            # Update Lat and Lon fields using the coordinates
            row[1] = y  # Latitude
            row[2] = x  # Longitude
            cursor.updateRow(row)

def export_featureclass_to_csv(gdb_path, featureclass_name, csv_path):
    arcpy.env.workspace = gdb_path
    featureclass_path = f"{gdb_path}\\{featureclass_name}"
    fields = [field.name for field in arcpy.ListFields(featureclass_path)]
    data = [row for row in arcpy.da.SearchCursor(featureclass_path, fields)]
    df = pd.DataFrame(data, columns=fields)
    
    # Replace NaN with empty string for export
    df = df.replace({np.nan: None})
    
    df.to_csv(csv_path, sep=';', index=False, encoding='utf-8')

# Parameters
gdb_path = r"F:\EHESS\Workbench\Geodata\Alcedo.gdb"
featureclass_name = "Alcedo_Places_from_Access"
csv_path = r"F:\EHESS\Workbench\processing\Output\Alcedo_geo.csv"

# Update Lat and Lon fields from geometry
update_lat_lon_from_geometry(gdb_path, featureclass_name)

# Export feature class to CSV
export_featureclass_to_csv(gdb_path, featureclass_name, csv_path)
