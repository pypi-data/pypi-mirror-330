import rasterio
from rasterio.enums import Resampling
from senphora.logger import logger

def resample(image_path):
    with rasterio.open(image_path, 'r+') as dataset:
        overviews = [2, 4, 8, 16]  # Define the overview levels you want to create
        dataset.build_overviews(overviews, Resampling.average)
    logger.info(f"Ресэмплинг завершен. Итоговое изображение пересохранено: {image_path}")