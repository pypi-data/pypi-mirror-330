import requests
import os
from datetime import datetime
from tqdm import tqdm
from senphora.exceptions import ProductNotFoundError, ProductNotLoadedError
from senphora.logger import logger

def load_product(access_token, product):
    """
    Загружает продукт.
    :param access_token:
    :param product:
    :return:
    :zip_file_path Путь к архиву
    :parent_folder Папка в которой находится архив
    """
    url = f"https://download.dataspace.copernicus.eu/odata/v1/Products({product['Id']})/$value"
    headers = {"Authorization": f"Bearer {access_token}"}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, stream=True)
    # Check if the request was successful
    if response.status_code == 200:
        logger.info(f"Получили добро на загрузку файла. response_status_code: {response.status_code}")
        date_str = product['ContentDate']['Start']
        date_obj = datetime.fromisoformat(date_str.rstrip('Z'))
        tile_name = get_tile_name(product['Name'])
        parent_folder = os.path.join(r"D:\Programming\1_Projects\fleet_commander",
            'data',
            str(date_obj.year),  # Год
            f"{date_obj.month:02d}",  # Месяц (с ведущим нулем)
            f"{date_obj.day:02d}", # День(с ведущим нулем)
            f"{tile_name}_{date_obj.hour:02d}_{date_obj.minute:02d}_{date_obj.second:02d}" #имя_тайла_Часы:минуты:секунды
        )
        # Выводим результат
        file_name = 'product.zip'
        zip_file_path = os.path.join(parent_folder, file_name)
        logger.info("Путь для сохранения файла:", zip_file_path)
        # Создаем директории, если они не существуют
        os.makedirs(os.path.dirname(zip_file_path), exist_ok=True)
        total_size = int(response.headers.get('content-length', 0))

        with open(zip_file_path, "wb") as file:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=zip_file_path) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive new chunks
                        file.write(chunk)
                        pbar.update(len(chunk))
        print("Загрузка завершена")
        if os.path.exists(zip_file_path):
            logger.info(f"Файл успешно загружен {zip_file_path}")
        else:
            raise ProductNotLoadedError(f"Файл {zip_file_path} не был загружен.")
        return zip_file_path, parent_folder
    else:
        raise ProductNotFoundError(f"Failed to download file. Status code: {response.status_code}, {response.text}")

def get_tile_name(name):
    strings = name.split("_")
    sattelite_name = strings[0]+"_"
    sattelite_proceessing_level = strings[1]+"_"
    sattelite_tile = strings[5]
    full_name = [sattelite_name, sattelite_proceessing_level, sattelite_tile]
    result = "".join(full_name)
    return result

if __name__ == "__main__":
    name = "S2B_MSIL2A_20250205T072009_N0511_R006_T39RTN_20250205T081649.SAFE"
    result = get_tile_name(name)
    print(result)
