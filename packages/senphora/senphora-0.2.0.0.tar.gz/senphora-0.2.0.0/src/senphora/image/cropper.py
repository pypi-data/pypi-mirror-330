import os

import numpy as np
import rasterio
from tqdm import tqdm
from ..polygon import read_polygon
from pyproj import Transformer
from rasterio.crs import CRS
from rasterio.mask import mask
from rasterio.windows import Window
from shapely.geometry import Polygon, mapping
from .format import resample
from senphora.logger import logger


def crop_image_by_polygon(image_path, output_image_path, polygon_coords):
    """
    Crop image by polygon coordinates
    :param image_path: путь до изображения
    :param product_folder: корневая папка продукта
    :param polygon_coords: координаты полигона
    :return:
    """
    # Преобразование координат полигона из EPSG:4326 в EPSG:32636
    with rasterio.open(image_path) as src:
        raster_crs = src.crs  # Получаем CRS растра (должно быть EPSG:32636)
        # Преобразование координат
        transformer = Transformer.from_crs(CRS.from_epsg(4326), raster_crs, always_xy=True)
        transformed_coords = [transformer.transform(x, y) for x, y in polygon_coords]
        polygon_geom = Polygon(transformed_coords)

        # Проверка пересечения полигонов
        raster_bounds = src.bounds
        if not Polygon.from_bounds(*raster_bounds).intersects(polygon_geom):
            raise ValueError("Полигон не пересекается с растровым изображением.")

        # Обрезка изображения по полигону
        geoms = [mapping(polygon_geom)]
        out_image, out_transform = mask(src, geoms, crop=True)

        # Копирование метаданных
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",  # Формат выходного файла
            "height": out_image.shape[1],  # Высота обрезанного изображения
            "width": out_image.shape[2],  # Ширина обрезанного изображения
            "transform": out_transform,  # Новая матрица трансформации
            "count": src.count,  # Число каналов (должно быть 3 для RGB)
            "dtype": src.dtypes[0]  # Тип данных (например, uint8)
        })

    # Сохранение обрезанного изображения
    with rasterio.open(output_image_path, "w", **out_meta) as dest:
        dest.write(out_image)  # Записываем все каналы

    logger.info(f"Обрезанное изображение сохранено: {output_image_path}")
    return output_image_path

def crop_image_by_lat_lon(image_path, output_image_path, lat, lon, img_size=640):
    with rasterio.open(image_path) as src:
        raster_crs = src.crs
        print(f"Растровая система координат: {raster_crs}")
        # Преобразование координат из EPSG:4326 в систему координат растра
        transformer = Transformer.from_crs(CRS.from_epsg(4326), raster_crs, always_xy=True)
        x_center, y_center = transformer.transform(lon, lat)
        # Проверка, что центр попадает внутрь растра
        if not (
                src.bounds.left <= x_center <= src.bounds.right and src.bounds.bottom <= y_center <= src.bounds.top):
            raise ValueError("Указанный центр вне области растрового изображения.")
        # Размер стороны квадрата в пикселях
        square_size = img_size
        half_size = square_size // 2

        # Определяем индексы пикселей для обрезки
        row_start = int(src.height - (y_center - src.bounds.bottom) / src.res[1] - half_size)
        row_stop = row_start + square_size
        col_start = int((x_center - src.bounds.left) / src.res[0] - half_size)
        col_stop = col_start + square_size

        # Корректируем границы, чтобы они не выходили за пределы растра
        row_start_clipped = max(0, row_start)
        row_stop_clipped = min(src.height, row_stop)
        col_start_clipped = max(0, col_start)
        col_stop_clipped = min(src.width, col_stop)

        # Создаем окно обрезки
        window = Window(col_start_clipped, row_start_clipped,
                        col_stop_clipped - col_start_clipped,
                        row_stop_clipped - row_start_clipped)

        # Читаем данные из растра
        out_image = src.read(window=window)

        # Создаем новое изображение размером 640x640, заполненное черным цветом
        full_image = np.zeros((src.count, square_size, square_size), dtype=src.dtypes[0])

        # Вычисляем смещение для вставки обрезанного фрагмента
        row_offset = max(0, -row_start)
        col_offset = max(0, -col_start)

        # Вставляем обрезанный фрагмент в новое изображение
        full_image[:, row_offset:row_offset + out_image.shape[1],
        col_offset:col_offset + out_image.shape[2]] = out_image

        # Вычисляем новую матрицу трансформации
        new_transform = rasterio.transform.from_bounds(
            src.bounds.left + col_start * src.res[0],
            src.bounds.bottom + (src.height - row_stop) * src.res[1],
            src.bounds.left + col_stop * src.res[0],
            src.bounds.bottom + (src.height - row_start) * src.res[1],
            width=square_size,
            height=square_size
        )

        # Копируем метаданные
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",  # Формат выходного файла
            "height": square_size,  # Высота обрезанного изображения
            "width": square_size,  # Ширина обрезанного изображения
            "transform": new_transform,  # Новая матрица трансформации
            "count": src.count,  # Число каналов (должно быть 3 для RGB)
            "dtype": src.dtypes[0]  # Тип данных (например, uint8)
        })

        # Сохраняем обрезанное изображение
        with rasterio.open(output_image_path, "w", **out_meta) as dest:
            dest.write(full_image)

        print(f"Тайл сохранен: {output_image_path}")
        return output_image_path

def remove_black_borders(input_image_path, output_img_path, nodata_value=0):
    with rasterio.open(input_image_path) as src:
        # Чтение данных растра
        image = src.read()
        height, width = src.height, src.width
        transform = src.transform

        # Поиск непустых пикселей
        mask = (image != nodata_value).any(axis=0)  # Маска непустых пикселей
        rows = mask.any(axis=1)  # Непустые строки
        cols = mask.any(axis=0)  # Непустые столбцы

        # Определение границ непустой области
        row_start, row_end = rows.argmax(), len(rows) - rows[::-1].argmax()
        col_start, col_end = cols.argmax(), len(cols) - cols[::-1].argmax()

        # Создание окна обрезки
        window = Window(col_start, row_start, col_end - col_start, row_end - row_start)

        # Обрезка данных и обновление трансформации
        cropped_image = src.read(window=window)
        updated_transform = rasterio.windows.transform(window, transform)

        # Обновление метаданных
        out_meta = src.meta.copy()
        out_meta.update({
            "height": cropped_image.shape[1],
            "width": cropped_image.shape[2],
            "transform": updated_transform,
            "nodata": nodata_value
        })

        # Сохранение обрезанного изображения
        with rasterio.open(output_img_path, "w", **out_meta) as dest:
            dest.write(cropped_image)
    logger.info(f"Черные пиксели преобразованы. Результат сохранен в {output_img_path}")
    return output_img_path


def split_jp2_into_tiles(input_img_path, tiles_dir, base_tile_name, tile_size=640):
    # Открываем JP2 файл
    with rasterio.open(input_img_path) as src:
        width, height = src.width, src.height
        transform = src.transform
        crs = src.crs

        # Создаем трансформер для преобразования в WGS84
        transformer = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)

        # Вычисляем новые размеры для кратности tile_size
        new_width = ((width + tile_size - 1) // tile_size) * tile_size
        new_height = ((height + tile_size - 1) // tile_size) * tile_size

        # Если размеры уже кратны tile_size, ничего не меняем
        if new_width == width and new_height == height:
            padded_data = src.read()
            updated_transform = transform
        else:
            # Читаем исходные данные
            data = src.read()

            # Создаем массив для расширенного изображения
            padded_data = np.zeros((data.shape[0], new_height, new_width), dtype=data.dtype)

            # Копируем исходные данные в новый массив
            padded_data[:, :height, :width] = data

            # Обновляем матрицу трансформации
            updated_transform = rasterio.Affine(
                transform.a, transform.b, transform.c,
                transform.d, transform.e, transform.f
            )

        # Вычисляем общее количество блоков
        total_blocks = (height // tile_size + (height % tile_size > 0)) * \
                       (width // tile_size + (width % tile_size > 0))
        # Проходим по всем блокам с помощью tqdm для отображения прогресса
        block_count = 0
        # Проходим по всем блокам с помощью tqdm для отображения прогресса
        with tqdm(total=total_blocks, desc="Обработка блоков", unit="блок") as pbar:
            for row in range(0, height, tile_size):
                for col in range(0, width, tile_size):
                    block_count += 1
                    # Определяем размер текущего блока
                    window = Window(col, row, min(tile_size, new_width - col), min(tile_size, new_height - row))

                    # Читаем данные блока
                    tile_data = padded_data[:, window.row_off:window.row_off + window.height,
                                window.col_off:window.col_off + window.width]

                    # Получаем географические координаты верхнего левого угла блока
                    ul_x, ul_y = rasterio.transform.xy(updated_transform, row, col)

                    # Преобразуем координаты в WGS84
                    wgs84_x, wgs84_y = transformer.transform(ul_x, ul_y)

                    # Формируем имя файла с координатами
                    tile_name = f"tile_{base_tile_name}_{wgs84_x:.6f}_{wgs84_y:.6f}.jp2"
                    output_tile = os.path.join(tiles_dir, tile_name)

                    # Копируем метаданные
                    out_meta = src.meta.copy()
                    out_meta.update({
                        "driver": "GTiff",
                        "height": window.height,
                        "width": window.width,
                        "transform": rasterio.windows.transform(window, updated_transform),
                    })

                    # Сохраняем блок
                    with rasterio.open(output_tile, "w", **out_meta) as dst:
                        dst.write(tile_data)

                    # Обновляем прогресс-бар
                    pbar.update(1)
                # print(f"Сохранен блок: {output_path}")
    logger.info(f"Разбиение на тайлы завершено. Тайлы сохранены в папку: {tiles_dir}")

if __name__ == "__main__":
    product_folder = '../data/2025/01/10/S2B_T43PDN_MSIL2A_05_21_09'
    filename = '../polygon_files/india_abma.geojson'
    polygon_coords = read_polygon(filename)
    crop_image_by_polygon(product_folder, polygon_coords)
    final_cropped_image = remove_black_borders(product_folder)
    resample(final_cropped_image)
    split_jp2_into_tiles(product_folder)
