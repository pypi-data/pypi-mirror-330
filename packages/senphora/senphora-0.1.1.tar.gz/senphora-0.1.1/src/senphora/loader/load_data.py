import requests
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from tqdm import tqdm
import re
from utils.exceptions import NotFoundError

def load_product(access_token, product):
    url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({product['Id']})/$value"
    headers = {"Authorization": f"Bearer {access_token}"}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        print("Получили добро на загрузку файла")
        date_str = product['ContentDate']['Start']
        date_obj = datetime.fromisoformat(date_str.rstrip('Z'))
        # Регулярное выражение для поиска тайла в формате TXXXX
        tile_name = get_tile_name(product['Name'])
        save_path = os.path.join(os.getcwd(),
            'data',
            str(date_obj.year),  # Год
            f"{date_obj.month:02d}",  # Месяц (с ведущим нулем)
            f"{date_obj.day:02d}", # День(с ведущим нулем)
            f"{tile_name}_{date_obj.hour:02d}_{date_obj.minute:02d}_{date_obj.second:02d}" #имя_тайла_Часы:минуты:секунды
        )
        # Выводим результат
        file_name = 'product.zip'
        file_path = os.path.join(save_path, file_name)
        print("Путь для сохранения файла:", file_path)
        # Создаем директории, если они не существуют
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(file_path, "wb") as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_path) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        pbar.update(len(chunk))
        print("Загрузка завершена")
        return file_path, save_path
    else:
        print(f"Failed to download file. Status code: {response.status_code}")
        print(response.text)
        raise NotFoundError

def get_tile_name(name):
    # Регулярное выражение для поиска тайла в формате TXXXX
    strings = name.split("_")
    satellit_name = strings[0] + "_"
    tile = strings[5] + "_"
    processing_level = strings[1]
    full_name = [satellit_name, tile, processing_level]
    result = "".join(full_name)
    return result

if __name__ == "__main__":
    name = "S2B_MSIL2A_20250205T072009_N0511_R006_T39RTN_20250205T081649.SAFE"
    result = get_tile_name(name)
    print(result)
