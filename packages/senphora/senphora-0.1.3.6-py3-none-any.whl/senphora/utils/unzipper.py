import zipfile
import os
from tqdm import tqdm


def unzip(zip_file_path, save_path):
    # Path to the ZIP file
    # Directory to extract the files
    extract_dir = os.path.join(os.getcwd(), save_path, 'product_files')

    # Create the extraction directory if it doesn't exist
    if not os.path.exists(extract_dir):
        os.makedirs(extract_dir)

    # Unzip the file
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        file_list = zip_ref.namelist()

        with tqdm(total=len(file_list), unit="file", desc="Extracting") as pbar:
            for file in file_list:
                zip_ref.extract(file, extract_dir)
                pbar.update(1)
    print("Распаковка завершена")

