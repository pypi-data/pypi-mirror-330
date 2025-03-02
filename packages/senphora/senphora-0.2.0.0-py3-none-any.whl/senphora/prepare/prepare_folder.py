from senphora.loader import load_product
from senphora.utils import unzip
from senphora.finder import find_img_folder_in_product, find_tci_path, find_jp2_files_in_folder
from senphora.image import crop_image_by_polygon, remove_black_borders, resample, split_jp2_into_tiles, convert_files_to_png
from senphora.logger import logger
from dataclasses import dataclass
import os


def load_and_unzip(access_token, product):
    """
    Load and unzip product
    :param access_token:
    :param product:
    :return:
    """
    zip_file_path, extract_dir = load_product(access_token, product)
    unzip(zip_file_path, extract_dir)
    return extract_dir

def crop_folder(product_folder):
    """
    Prepare folder for cropped image
    :param product_folder: Folder with product.zip and unpacked folder
    :return:
    """
    output_image_folder = os.path.join(product_folder, "cropped")
    cropped_name = 'cropped.jp2'
    blacked_name = 'blacked.jp2'
    cropped_image_path = os.path.join(output_image_folder, cropped_name)
    blacked_image_path = os.path.join(output_image_folder, blacked_name)
    os.makedirs(output_image_folder, exist_ok=True)
    logger.info(f"Папка для обрезки подготовлена: {output_image_folder}")
    return cropped_image_path, blacked_image_path

def tiles_folder(product_folder):
    """
    Prepare tiles folder for cropped image
    :param product_folder: Folder with product.zip and unpacked folder
    :return:
    """
    output_dir = os.path.join(product_folder, 'tiles')
    base_tiles_name = os.path.basename(os.path.normpath(product_folder)) # - название предпоследней папки
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Папка для тайлов подготовлена: {output_dir}")
    return output_dir, base_tiles_name

def png_folder(product_folder):
    """
    Prepare folder for png_tiles
    :param product_folder: Folder with product.zip and unpacked folder
    :return:
    """
    output_dir = os.path.join(product_folder, 'png_data')
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Папка для png подготовлена: {output_dir}")
    return output_dir

def tci_image_path(product_folder):
    """
    Prepare path to tci image
    :param product_folder: Folder with product.zip and unpacked folder
    :return:
    """
    tci_folder = find_img_folder_in_product(product_folder)
    tci_image = find_tci_path(tci_folder)
    logger.info(f"TCI изображение найдено: {tci_image}")
    return tci_image

@dataclass
class PrepareFolders:
    """
    class for preparing folders
    :param cropped_img: path to cropped image
    :param blacked_img: path to blacked image
    :param tci_img: path to tci image
    :param tiles_dir: path to tiles folder
    :param tiles_base_name: base name of tiles folder
    :param png_dir: path to png folder
    """
    cropped_img: str
    blacked_img: str
    tci_img: str
    tiles_base_name: str
    tiles_dir: str
    png_dir: str


def prepare_folders_neuro(product_folder: str) -> PrepareFolders:
    """
    Prepare folders for neural network
    :param product_folder:
    :return:
    """
    cropped_img_path, blacked_img_path = crop_folder(product_folder)
    tiles_dir, base_tile_name = tiles_folder(product_folder)
    png_dir = png_folder(product_folder)
    tci_image = tci_image_path(product_folder)
    prepared_folders = PrepareFolders(
        cropped_img = cropped_img_path,
        blacked_img = blacked_img_path,
        tiles_dir = tiles_dir,
        tiles_base_name = base_tile_name,
        png_dir = png_dir,
        tci_img = tci_image
    )
    return prepared_folders

def prepare_img_neuro(prepared_folders: PrepareFolders, polygon_coords: list):
    """
    Prepare image for neural network
    :param prepared_folders: PreparedFolders class
    :param polygon_coords: list of coordinates of polygon
    :return:
    """
    crop_image_by_polygon(prepared_folders.tci_img, prepared_folders.cropped_img, polygon_coords)
    remove_black_borders(prepared_folders.cropped_img, prepared_folders.blacked_img)
    resample(prepared_folders.blacked_img)
    split_jp2_into_tiles(prepared_folders.blacked_img, prepared_folders.tiles_dir, prepared_folders.tiles_base_name)
    jp2_files = find_jp2_files_in_folder(prepared_folders.tiles_dir)
    png_dir = convert_files_to_png(jp2_files, prepared_folders.png_dir)
    return png_dir