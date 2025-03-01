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

# Вспомогательная функция для получения всех записей с нужным индексом
def get_data_by_index(data_dict, filtered_indexies):
    filtered_data = {}
    for key_name, value in data_dict.items():
        # print(f'{key_name} : {value}')
        filtered_data_items = {key: value for key, value in data_dict[key_name].items() if key in filtered_indexies}
        filtered_data[key_name] = filtered_data_items
    return filtered_data

def get_flat_data(data):
    # Определяем индекс (предполагаем, что все ключи имеют одинаковый индекс)
    index = next(iter(data.values())).keys().__iter__().__next__()

    # Преобразуем словарь, убирая индекс
    flat_data = {key: value[index] for key, value in data.items()}
    return flat_data


def filter_products_by_l2a(product_dict):
    filtered_products_id = {key: value for key, value in product_dict['Name'].items() if "L2A" in value}
    filtered_indecies = [key for key in filtered_products_id.keys()]

    filtered_products = get_data_by_index(product_dict, filtered_indecies)
    print(f"Число результатов l2a:{len(filtered_products['Name'])}" )
    return filtered_products


def filter_latest_product(product_dict):
    product_dates = product_dict['ContentDate']
    parsed_dates = {
        index: datetime.fromisoformat(value['Start'].rstrip('Z'))
        for index, value in product_dates.items()
    }
    latest_index = [max(parsed_dates, key=parsed_dates.get)]

    latest_product = get_data_by_index(product_dict, latest_index)
    flat_data = get_flat_data(latest_product)
    return flat_data


if __name__ == '__main__':
    lat = '31.52174'
    lon = '32.36212'
    collection_name = 'SENTINEL-2'
    data_start = '2025-01-01T00:00:00.000Z'
    data_end = '2025-01-20T00:00:00.000Z'
    product_dict = products_by_coords(lon=lon, lat=lat, collection_name=collection_name,
                                                    data_start=data_start, data_end=data_end)
    #Фильруем l2a
    l2a_products = filter_products_by_l2a(product_dict)

    # Фильтруем ближайший архив
    latest_product = filter_latest_product(l2a_products)
    print(latest_product['GeoFootprint'])
