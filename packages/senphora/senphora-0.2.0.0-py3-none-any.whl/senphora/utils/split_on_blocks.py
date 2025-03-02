import rasterio
from rasterio.windows import Window
import os
from tqdm import tqdm


def split_on_blocks(product_folder, block_size = 512):
    image_path = os.path.join(product_folder, 'output.tif')

    # Создаем папку для сохранения блоков
    output_folder = os.path.join(product_folder, 'output_blocks')
    os.makedirs(output_folder, exist_ok=True)
    # Открываем файл с помощью rasterio
    with rasterio.open(image_path) as src:
        # Получаем размеры изображения
        height, width = src.shape

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
                  desc=f"{GREEN}Разбиение на блоки{RESET}",
                  bar_format=CUSTOM_BAR_FORMAT,
                  unit="block",
                  ) as pbar:
            # Проходим по изображению и вырезаем блоки
            for i in range(0, height, block_size):
                for j in range(0, width, block_size):
                    # Определяем окно (блок)
                    window = Window(j, i, min(block_size, width - j), min(block_size, height - i))

                    # Читаем данные для текущего блока
                    block_data = src.read(window=window)

                    # Сохраняем блок в файл
                    block_path = os.path.join(output_folder, f'block_{i}_{j}.tif')
                    with rasterio.open(block_path, 'w',
                                       driver='GTiff',
                                       width=window.width,
                                       height=window.height,
                                       count=src.count,  # Количество каналов
                                       dtype=block_data.dtype,
                                       crs=src.crs,  # Система координат
                                       transform=src.window_transform(window)) as dst:
                        dst.write(block_data)
                    pbar.update(1)

    print(f"Изображение разбито на блоки и сохранено в папку '{output_folder}'.")

if __name__ == '__main__':
    product_folder = "../data/2025/01/19/09_12_19/product_files"
    split_on_blocks(product_folder)