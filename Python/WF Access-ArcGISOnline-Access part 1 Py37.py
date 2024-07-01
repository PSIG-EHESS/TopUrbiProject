##This script serves to export updated features from the collective editing webmap for localizing indigenous nations.
##Script written by ChatGPT 4


from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pandas as pd

def export_featurelayer_to_csv(feature_service_url, csv_path):
    # Connect to ArcGIS Online anonymously
    gis = GIS()
    
    # Access the feature layer
    feature_layer = FeatureLayer(feature_service_url)
    
    # Query all features
    features = feature_layer.query(where='1=1', out_fields='*', return_geometry=False).features
    
    # Convert features to a DataFrame
    data = [f.attributes for f in features]
    df = pd.DataFrame(data)
    
    # Replace NaN with empty string for export
    df = df.where(pd.notnull(df), None)
    
    # Export to CSV
    df.to_csv(csv_path, sep=';', index=False, encoding='utf-8')

# Parameters
feature_service_url = "https://services2.arcgis.com/fKO2K6qiLNlgkZ2U/arcgis/rest/services/Alcedo_Indiens_WFL1/FeatureServer/0"
csv_path = r"F:\EHESS\Workbench\processing\Output\Alcedo_geo_web.csv"

# Export feature layer to CSV
export_featurelayer_to_csv(feature_service_url, csv_path)
