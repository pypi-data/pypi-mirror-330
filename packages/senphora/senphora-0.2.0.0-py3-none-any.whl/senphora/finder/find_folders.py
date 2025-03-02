import glob
import os
import shutil
import hashlib
from senphora.exceptions import TooManyFoldersError
from senphora.logger import logger

def find_img_folder_in_product(product_path):
    """Function for searching img folder in product.
    :param product_path: Folder with unpacked product.
    :return img_folder_path: Folder with unpacked img folder.
    """
    r10m_folders = find_r10m_folder(product_path)
    match len(r10m_folders):
        case 0:
            print("Папка R10m не найдена.")
            img_folders = find_img_folder(product_path)
            match len(img_folders):
                case 0:
                    print("Папка IMG_DATA не найдена.")
                case  1:
                    print(f"Найдена ровно одна папка IMG: {img_folders}")
                    return img_folders[0]
                case _ if  len(img_folders) > 1:
                    raise TooManyFoldersError(f"Ошибка: Найдено несколько папок IMG: {img_folders}")
        case 1:
            # Если найдена ровно одна папка R10m
            print(f"Найдена папка R10m: {r10m_folders}")
            return r10m_folders[0]
        case _ if len(r10m_folders) > 1:
            raise TooManyFoldersError(f"Ошибка: Найдено несколько папок R10m: {r10m_folders}")

def find_r10m_folder(product_path):
    """Function for finding r10m folder
    :param product_path:
    :return r10m_folder
    """
    r10m_pattern = os.path.join(product_path, "**", "IMG_DATA", "R10m")
    r10m_folders = glob.glob(r10m_pattern, recursive=True)
    return r10m_folders

def find_img_folder(product_path):
    """Function for finding img folder
    :param product_path:
    :return img_folder
    """
    img_pattern = os.path.join(product_path, "**", "IMG_DATA")
    img_folders = glob.glob(img_pattern, recursive=True)
    return img_folders

def find_tci_path(picture_path):
    """Function for finding tci path
    :param picture_path: Folder with images
    :return tci_path
    """
    # Проверяем, существует ли папка
    if not os.path.exists(picture_path):
        raise FileNotFoundError(f"Папка {picture_path} не существует.")

    # Проходим по всем файлам в папке
    for root, dirs, files in os.walk(picture_path):
        for file in files:
            # Проверяем, что файл имеет расширение .jp2 и содержит 'TCI' в названии
            if file.endswith(".jp2") and "TCI" in file:
                return os.path.join(root, file)  # Возвращаем полный путь к файлу
    # Если файл не найден, возвращаем None
    return None

def find_detections_png_files(data_dir):
    detection_pattern = os.path.join(data_dir, "**", "detections")
    detection_folders = glob.glob(detection_pattern, recursive=True)
    png_files = []
    for folder in detection_folders:
        if not os.path.exists(folder):
            print(f"Предупреждение: папка '{folder}' не существует.")
            continue
        png_files_in_folder = find_png_files_in_folder(folder)
        for png_file in png_files_in_folder:
            png_files.append(png_file)
        # for root, _, files in os.walk(folder):
        #     for file in files:
        #         # Проверяем, что файл имеет расширение .jp2 и содержит 'TCI' в названии
        #         if file.lower().endswith('.png'):  # Ищем файлы с расширением .png
        #             full_path = os.path.join(root, file)
        #             png_files.append(full_path)
    return png_files

def find_png_files_in_folder(png_dir):
    png_files = []
    for root, _, files in os.walk(png_dir):
        for file in files:
            # Проверяем, что файл имеет расширение .jp2 и содержит 'TCI' в названии
            if file.lower().endswith('.png'):  # Ищем файлы с расширением .png
                full_path = os.path.join(root, file)
                png_files.append(full_path)
    return png_files


def find_tiles_files(data_dir):
    tiles_pattern = os.path.join(data_dir, "**", "tiles")
    tiles_folders = glob.glob(tiles_pattern, recursive=True)
    jp2_files = []
    for folder in tiles_folders:
        if not os.path.exists(folder):
            print(f"Предупреждение: папка '{folder}' не существует.")
            continue
        jp2_files_in_folder = find_jp2_files_in_folder(folder)
        for jp2_file in jp2_files_in_folder:
            jp2_files.append(jp2_file)
    return jp2_files

def find_jp2_files_in_folder(jp2_dir):
    jp2_files = []
    for root, _, files in os.walk(jp2_dir):
        for file in files:
            # Проверяем, что файл имеет расширение .jp2 и содержит 'TCI' в названии
            if file.lower().endswith('.jp2'):  # Ищем файлы с расширением .png
                full_path = os.path.join(root, file)
                jp2_files.append(full_path)
    logger.info(f"Файлов jp2 обнаружено в папке: {len(jp2_files)}")
    return jp2_files

def find_matching_jp2_files(png_file_paths, jp2_file_paths):
    png_names = {os.path.splitext(os.path.basename(path))[0] for path in png_file_paths}
    # Ищем .jp2-файлы с такими же именами
    matching_jp2_files = []
    for jp2_path in jp2_file_paths:
        jp2_name, _ = os.path.splitext(os.path.basename(jp2_path))
        if jp2_name in png_names:
            matching_jp2_files.append(jp2_path)
    return matching_jp2_files


def copy_file_to_folder(files_path, destination_folder):
    # Создаем целевую папку, если её нет
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for file_path in files_path:
        if not os.path.isfile(file_path):
            print(f"Предупреждение: файл '{file_path}' не существует или это не файл.")
            continue

        # Формируем имя файла в целевой папке
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_folder, file_name)

        try:
            shutil.copy2(file_path, destination_path)  # Используем copy2 для сохранения метаданных
        except Exception as e:
            print(f"Ошибка при копировании файла {file_path}: {e}")

def remove_duplicate_files(folder_path):
    """
    Удаляет дублирующиеся файлы в указанной папке.

    :param folder_path: Путь к папке, где нужно найти и удалить дубликаты.
    """
    hash_dict = {}  # Словарь для хранения хешей файлов

    # Функция для вычисления хеша файла
    def get_file_hash(file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):  # Читаем файл блоками по 8 КБ
                hasher.update(chunk)
        return hasher.hexdigest()

    # Обходим все файлы в папке
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                file_hash = get_file_hash(file_path)  # Вычисляем хеш файла

                if file_hash in hash_dict:
                    print(f"Найден дубликат: {file_path}")
                    os.remove(file_path)  # Удаляем дубликат
                    print(f"Удален файл: {file_path}")
                else:
                    hash_dict[file_hash] = file_path  # Добавляем файл в словарь
            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")
