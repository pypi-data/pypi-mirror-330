import os
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image

from .find_folders import find_jp2_files_in_folder


def convert_all_files_in_folder(train_folder_path):
    folder_path = Path(train_folder_path)
    parent_path = folder_path.parent
    output_folder = os.path.join(parent_path, "png_data")
    os.makedirs(output_folder, exist_ok=True)
    jp2_files = find_jp2_files_in_folder(train_folder_path)
    for jp2_file in jp2_files:
        input_path = jp2_file
        file_name = os.path.basename(input_path)
        name_without_ext, ext = os.path.splitext(file_name)
        new_file_name = name_without_ext + ".png"
        output_path = os.path.join(output_folder, new_file_name)
        convert_jp2_to_png(input_path, output_path)
    return output_folder

def convert_jp2_to_png(input_path, output_path):
    """
    Преобразует файл .jp2 в файл .png без потери качества.

    :param input_path: Путь к входному файлу .jp2
    :param output_path: Путь к выходному файлу .png
    """
    try:
        # Открываем JP2 файл с помощью rasterio
        with rasterio.open(input_path) as src:
            # Читаем данные всех каналов
            data = src.read()

            # Проверяем количество каналов
            if data.shape[0] > 3:
                print(
                    "Внимание: Исходное изображение содержит более 3 каналов. Будут использованы только первые 3 (R, G, B).")
                data = data[:3]  # Выбираем только первые три канала (R, G, B)

            # Транспонируем данные для совместимости с Pillow (каналы должны быть последней осью)
            image_data = np.transpose(data, (1, 2, 0))

            # Конвертируем данные в формат uint8 (если они еще не в этом формате)
            if image_data.dtype != np.uint8:
                image_data = ((image_data - image_data.min()) / (image_data.max() - image_data.min()) * 255).astype(
                    np.uint8)

            # Создаем изображение с помощью Pillow
            image = Image.fromarray(image_data)

            # Сохраняем изображение в формате PNG
            image.save(output_path, format="PNG")

        # print(f"Файл успешно преобразован: {output_path}")

    except Exception as e:
        print(f"Ошибка при преобразовании файла: {e}")

if __name__ == "__main__":
    # Папка с тайлами
    train_folder = "../data/detections/matching_jp2/"
    jp2_files = find_jp2_files_in_folder(train_folder)
    print(len(jp2_files))
    # file_name = '../data/train_data/bare_data\\tile_-76.312922_37.017280.jp2'
    # output_path = '../data/train_data/png_data\\tile_-76.312922_37.017280.png'
    # convert_jp2_to_png(file_name, output_path)
    convert_all_files_in_folder(train_folder)
