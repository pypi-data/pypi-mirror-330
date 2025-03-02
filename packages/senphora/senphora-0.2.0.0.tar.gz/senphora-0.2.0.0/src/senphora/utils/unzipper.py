import zipfile
import os
from tqdm import tqdm
from senphora.logger import logger

def unzip(zip_file_path, extract_dir):
    """
    Распаковывает архив в указанную директорию.

    :param zip_file_path: Путь к ZIP-архиву.
    :param extract_dir: Директория, куда будут извлечены файлы.
    """
    # Проверяем, существует ли архив
    if not os.path.exists(zip_file_path):
        raise FileNotFoundError(f"Архив {zip_file_path} не найден.")

    # Определяем директорию для распаковки
    unpack_dir = os.path.join(os.getcwd(), extract_dir, 'product_files')

    # Создаем директорию для извлечения, если она не существует
    os.makedirs(unpack_dir, exist_ok=True)

    # Распаковываем архив с прогресс-баром
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        # Получаем список всех файлов в архиве
        total_files = len(zip_ref.infolist())

        with tqdm(iterable=zip_ref.infolist(), total=total_files, unit="file", desc="Распаковка") as pbar:
            for file in pbar:
                zip_ref.extract(file, path=unpack_dir)
                pbar.set_description(f"Распаковка {file.filename}")
    logger.info(f"Архив {zip_file_path} успешно распакован в {unpack_dir}.")
    return unpack_dir
