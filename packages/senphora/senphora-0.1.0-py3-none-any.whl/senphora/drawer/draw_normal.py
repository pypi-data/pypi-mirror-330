import rasterio
from rasterio.windows import Window
import numpy as np
from rasterio.enums import ColorInterp, Resampling
import json
from utils.find_folders import find_channeles_files, find_channeles_folder
import os
from tqdm import tqdm

def read_normals(file_path):
    with open(file_path) as json_file:
        json_data =  json.load(json_file)
    return json_data


# Функция для нормализации данных
def normalize(band, band_min, band_max):
    return (band - band_min) / (band_max - band_min)

def draw_blocks(product_folder, block_size=1024):
    r_10m_folder = find_channeles_folder(product_folder)
    red_path, blue_path, green_path = find_channeles_files(r_10m_folder)
    normalz_file_path = os.path.join(product_folder,
                                     'normalz.json')
    # Открываем файлы
    with rasterio.open(red_path) as red, rasterio.open(green_path) as green, rasterio.open(blue_path) as blue:
        # Получаем размеры изображения
        height, width = red.shape
        output_file = os.path.join(product_folder,
                                  'output.tif')
        # Создаем выходной файл
        with rasterio.open(
                output_file,
            "w",
            driver="GTiff",
            height=height,
            width=width,
            count=3,
            dtype=np.float32,
            transform=red.transform,
            crs=red.crs,
            photometric="RGB",
        ) as dst:

            GREEN = "\033[92m"
            YELLOW = "\033[93m"
            BLUE = "\033[94m"
            RESET = "\033[0m"

            CUSTOM_BAR_FORMAT = (
                f"{GREEN}{{l_bar}}{RESET}"  # Левый символ (зеленый)
                f"{BLUE}{{bar}}{RESET}"  # Сам бар (синий)
                f"{GREEN}{{r_bar}}{RESET}"  # Правый символ (желтый)
            )

            total_blocks = ((height + block_size - 1) // block_size) * ((width + block_size - 1) // block_size)
            with tqdm(total=total_blocks,
                      desc=f"{GREEN}Отрисовка блоков{RESET}",
                      bar_format=CUSTOM_BAR_FORMAT,
                      unit="block"
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

                        #Читаем значения для нормализации
                        normals = read_normals(normalz_file_path)

                        # Нормализуем данные
                        red_norm = normalize(red_block, normals['red_norm_min'], normals['red_norm_max'])
                        green_norm = normalize(green_block, normals['green_norm_min'], normals['green_norm_max'])
                        blue_norm = normalize(blue_block, normals['blue_norm_min'], normals['blue_norm_max'])

                        # Создаем RGB-композит для текущего блока
                        rgb_block = np.dstack((red_norm, green_norm, blue_norm))

                        # Записываем данные в выходной файл
                        dst.write(rgb_block[:, :, 0], 1, window=window)  # Красный канал
                        dst.write(rgb_block[:, :, 1], 2, window=window)  # Зеленый канал
                        dst.write(rgb_block[:, :, 2], 3, window=window)  # Синий канал
                        pbar.update(1)

            # Устанавливаем цветовые интерпретации
            dst.colorinterp = [ColorInterp.red, ColorInterp.green, ColorInterp.blue]

    print(f"Обработка завершена. Результат сохранен в {output_file}")

# Функция для получения границ изображения
def get_image_bounds(image_path):
    with rasterio.open(image_path) as src:
        # Получаем границы изображения в координатах CRS
        bounds = src.bounds
        # Преобразуем границы в формат [[lat_min, lon_min], [lat_max, lon_max]]
        return [[bounds.bottom, bounds.left], [bounds.top, bounds.right]]

def resample(image_path):
    print(f"Ресэмплинг итогового изображения")
    with rasterio.open(image_path, 'r+') as dataset:
        overviews = [2, 4, 8, 16]  # Define the overview levels you want to create
        dataset.build_overviews(overviews, Resampling.average)
    print(f"Ресэмплинг завершен. Итоговое изображение пересохранено: {image_path}")


def find_non_black_bounds(src):
    # Читаем первый канал (красный) как массив
    red_band = src.read(1)

    # Создаем маску для ненулевых значений
    non_black_mask = red_band != 0

    # Если нет ненулевых данных, возвращаем None
    if not np.any(non_black_mask):
        return None

    # Находим границы по строкам и столбцам
    rows = np.any(non_black_mask, axis=1)
    cols = np.any(non_black_mask, axis=0)

    row_start, row_end = np.where(rows)[0][[0, -1]]
    col_start, col_end = np.where(cols)[0][[0, -1]]

    return row_start, row_end + 1, col_start, col_end + 1


def crop_tif(product_folder):
    input_file = os.path.join(product_folder,
                                     'output.tif')
    output_file = os.path.join(product_folder,
                                     'result.tif')
    with rasterio.open(input_file) as src:
        bounds = find_non_black_bounds(src)

        if bounds is None:
            print("Нет ненулевых данных для обрезки.")
            return

        row_start, row_end, col_start, col_end = bounds

        # Определяем окно для обрезки
        window = Window(col_start, row_start, col_end - col_start, row_end - row_start)

        # Читаем данные из окна
        data = src.read(window=window)

        # Создаем новый файл с теми же метаданными
        profile = src.profile
        profile.update(
            width=col_end - col_start,
            height=row_end - row_start,
            transform=rasterio.windows.transform(window, src.transform)
        )

        with rasterio.open(output_file, "w", **profile) as dst:
            dst.write(data)

    print(f"Обрезка завершена. Результат сохранен в {output_file}")


if __name__ == "__main__":
    image_path = "../data/2025/02/01/08_32_21/T36RVT/cropped/cropped_blacked.jp2"
    resample(image_path)