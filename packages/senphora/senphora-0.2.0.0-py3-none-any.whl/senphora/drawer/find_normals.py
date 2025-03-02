import rasterio
from rasterio.windows import Window
import numpy as np
from rasterio.enums import ColorInterp
from tqdm import tqdm
import json
import glob
import os
import sys
from utils.find_folders import find_channeles_files, find_channeles_folder

# Функция для нормализации данных
def normalize(band):
    band_min = band.min()
    band_max = band.max()
    return band_min, band_max

def clip_outliers(band, lower_percentile=2, upper_percentile=98):
    """
        Обрезает выбросы в канале на основе процентилей.
        """
    lower = np.percentile(band, lower_percentile)
    upper = np.percentile(band, upper_percentile)
    return np.clip(band, lower, upper)

def find_min_max_bands(product_folder, block_size=1024):
    r_10m_folder = find_channeles_folder(product_folder)
    red_path, blue_path, green_path = find_channeles_files(r_10m_folder)
    normalz_file_path = os.path.join(product_folder,
                                     'normalz.json')
    # Открываем файлы
    with rasterio.open(red_path) as red, rasterio.open(green_path) as green, rasterio.open(blue_path) as blue:
        # Получаем размеры изображения
        height, width = red.shape

        red_norm_min = None
        red_norm_max = None
        green_norm_min = None
        green_norm_max = None
        blue_norm_min = None
        blue_norm_max = None

        total_blocks = ((height + block_size - 1) // block_size) * ((width + block_size - 1) // block_size)

        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        RESET = "\033[0m"

        CUSTOM_BAR_FORMAT = (
            f"{GREEN}{{l_bar}}{RESET}"  # Левый символ (зеленый)
            f"{BLUE}{{bar}}{RESET}"  # Сам бар (синий)
            f"{GREEN}{{r_bar}}{RESET}"  # Правый символ (желтый)
        )

        with tqdm(total=total_blocks,
                  desc=f"{GREEN}Нормализация блоков{RESET}",
                  bar_format=CUSTOM_BAR_FORMAT,
                  unit="block",
                  ) as pbar:
            # Обрабатываем изображение по блокам
            for i in range(0, height, block_size):
                for j in range(0, width, block_size):
                    # Определяем окно для текущего блока
                    window = Window(j, i, min(block_size, width - j), min(block_size, height - i))

                    # Читаем данные для текущего блока
                    red_block = red.read(1, window=window)
                    green_block = green.read(1, window=window)
                    blue_block = blue.read(1, window=window)

                    red_block = clip_outliers(red_block, lower_percentile=2, upper_percentile=98)
                    green_block = clip_outliers(green_block, lower_percentile=2, upper_percentile=98)
                    blue_block = clip_outliers(blue_block, lower_percentile=2, upper_percentile=98)

                    # Нормализуем данные
                    red_norm_min_value, red_norm_max_value = normalize(red_block)
                    green_norm_min_value, green_norm_max_value = normalize(green_block)
                    blue_norm_min_value, blue_norm_max_value = normalize(blue_block)

                    if red_norm_min is None or red_norm_min_value < red_norm_min:
                        red_norm_min = red_norm_min_value
                    if red_norm_max is None or red_norm_max_value > red_norm_max:
                        red_norm_max = red_norm_max_value
                    if green_norm_min is None or green_norm_min_value < green_norm_min:
                        green_norm_min = green_norm_min_value
                    if green_norm_max is None or green_norm_max_value > green_norm_max:
                        green_norm_max = green_norm_max_value
                    if blue_norm_min is None or blue_norm_min_value < blue_norm_min:
                        blue_norm_min = blue_norm_min_value
                    if blue_norm_max is None or blue_norm_max_value > blue_norm_max:
                        blue_norm_max = blue_norm_max_value
                    pbar.update(1)

    normalz = {'red_norm_min':int(red_norm_min), 'red_norm_max':int(red_norm_max),
               'green_norm_min':int(green_norm_min), 'green_norm_max': int(green_norm_max),
               'blue_norm_min':int(blue_norm_min), 'blue_norm_max': int(blue_norm_max)}
    print(f"Обработка завершена. Результат сохранен в файл {normalz_file_path}")
    with open(normalz_file_path, 'w') as normalz_file:
        json.dump(normalz, normalz_file, ensure_ascii=False)
    return normalz_file_path

if __name__ == "__main__":

    product_folder = "../data/2025/02/06/08_30_29/T36RVV"
    find_min_max_bands(product_folder)
