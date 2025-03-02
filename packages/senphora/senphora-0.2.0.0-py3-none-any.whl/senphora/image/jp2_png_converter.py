import os

import numpy as np
import rasterio
from PIL import Image
from senphora.logger import logger


def convert_files_to_png(jp2_files, output_folder):
    for jp2_file in jp2_files:
        input_path = jp2_file
        file_name = os.path.basename(input_path)
        name_without_ext, ext = os.path.splitext(file_name)
        new_file_name = name_without_ext + ".png"
        output_path = os.path.join(output_folder, new_file_name)
        convert_jp2_to_png(input_path, output_path)
    logger.info(f"Конвертация файлов jp -> png прошла успешно. Результат сохранён: {output_folder}")
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
