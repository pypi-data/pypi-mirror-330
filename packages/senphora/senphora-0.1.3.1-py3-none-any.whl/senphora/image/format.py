import rasterio
from rasterio.enums import Resampling

def resample(image_path):
    print(f"Ресэмплинг итогового изображения")
    with rasterio.open(image_path, 'r+') as dataset:
        overviews = [2, 4, 8, 16]  # Define the overview levels you want to create
        dataset.build_overviews(overviews, Resampling.average)
    print(f"Ресэмплинг завершен. Итоговое изображение пересохранено: {image_path}")