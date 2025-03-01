import requests
from datetime import datetime
import pandas as pd
from ..polygon import coords_to_str

def products_by_polygon(polygon_coords:list, data_start:str, data_end:str,collection_name: str = "SENTINEL-2", top = 1000):
    polygon_coords = coords_to_str(polygon_coords)
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{collection_name}' and OData.CSC.Intersects(area=geography'SRID=4326;POLYGON({polygon_coords})') and ContentDate/Start gt {data_start} and ContentDate/Start lt {data_end}&$top={top}"
    json = requests.get(
        url).json()
    df = pd.DataFrame.from_dict(json['value'])
    pd.set_option('display.max_colwidth', None)
    print(f'Число результатов:{len(df)}')
    df_dict = df.to_dict()
    return df_dict

def products_by_coords(lat, lon, data_start, data_end, collection_name: str = "SENTINEL-2", top: int = 1000):
    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{collection_name}' and OData.CSC.Intersects(area=geography'SRID=4326;POINT({lon} {lat})') and ContentDate/Start gt {data_start} and ContentDate/Start lt {data_end}&$top={top}"
    json = requests.get(
        url).json()
    df = pd.DataFrame.from_dict(json['value'])
    pd.set_option('display.max_colwidth', None)
    print(f'Число результатов:{len(df)}')
    df_dict = df.to_dict()
    return df_dict
