import arcpy

def create_featureclass_from_csv(csv_path, gdb_path, featureclass_name, x_col, y_col):
    arcpy.env.workspace = gdb_path
    if arcpy.Exists(featureclass_name):
        arcpy.Delete_management(featureclass_name)
    spatial_ref = arcpy.SpatialReference(4326)  # Assuming WGS 84
    arcpy.management.XYTableToPoint(csv_path, featureclass_name, x_col, y_col, "", spatial_ref)


# Parameters
access_db_path = r"F:\EHESS\TopUrbi_2024.accdb"
table_name = "Alcedo_structured"
csv_path = r"F:\EHESS\Workbench\processing\Input\Alcedo_structured.csv"
gdb_path = r"F:\EHESS\Workbench\Geodata\Alcedo.gdb"
featureclass_name = "Alcedo_Places_from_Access"
x_col = "Lon"
y_col = "Lat"

# Create/Overwrite feature class in ESRI geodatabase
create_featureclass_from_csv(csv_path, gdb_path, featureclass_name, x_col, y_col)
