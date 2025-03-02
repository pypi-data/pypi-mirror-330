import json
import os

# Распаковка координат полигона
def read_polygon(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        geojson_data = json.load(file)
    feature = geojson_data["features"][0]  # Первый объект
    geometry = feature["geometry"]  # Геометрия первого объекта

    if geometry["type"] != "Polygon":
        raise ValueError("Геометрия не является Polygon.")
    file_polygon_coords = geometry["coordinates"][0]
    # Не свапаем при чтении для правильного запроса координат
    # Возвращаем координаты внешнего контура
    return file_polygon_coords

def coords_to_str(polygon_coords):
    # Форматируем каждую пару координат в "latitude longitude"
    formatted_coords = ["{:.8f} {:.8f}".format(lon, lat) for lon, lat in polygon_coords] # не свапаем для ODATA
    formatted_str_coords = f"({','.join(formatted_coords)})"
    return formatted_str_coords

def swap_polygon_coords(polygon_coords):
    swapped_lat_lon = [[point[1], point[0]] for point in polygon_coords]
    # Возвращаем координаты внешнего контура
    return swapped_lat_lon

def get_polygon_center(polygon_coords):
    total_lon = sum(point[0] for point in polygon_coords)
    total_lat = sum(point[1] for point in polygon_coords)
    n = len(polygon_coords)
    centroid_lon = total_lon / n
    centroid_lat = total_lat / n
    return centroid_lon, centroid_lat


def fix_coordinates(geojson_data):
    """
    Исправляет координаты, удаляя 360 из значений долготы.
    """
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Polygon':
            for polygon in feature['geometry']['coordinates']:
                for i, coord in enumerate(polygon):
                    while coord[0] < -180 or coord[0] > 180:
                        # Удаляем 360 из долготы
                        if coord[0] < -180:
                            coord[0] += 360
                        elif coord[0] > 180:
                            coord[0] -= 360
    return geojson_data


def save_fixed_geojson(input_file):
    """
    Читает GeoJSON из файла, исправляет координаты и сохраняет в новый файл.
    """
    output_file = os.path.join(os.path.dirname(input_file), "fixed_" + os.path.basename(input_file))
    with open(input_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)

    fixed_geojson = fix_coordinates(geojson_data)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_geojson, f, indent=4)


def correct_polygon_files_in_folder(input_folder):
    """
    Обходит все файлы в папке, находит GeoJSON файлы и обрабатывает их.
    """
    # Создаем выходную папку, если она не существует
    output_folder = input_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Обходим все файлы в папке
    for filename in os.listdir(input_folder):
        # Проверяем, что файл имеет расширение .geojson
        if filename.endswith('.geojson'):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, f"fixed_{filename}")

            # Обрабатываем файл
            save_fixed_geojson(input_file)
            print(f"Обработан файл: {filename} -> {output_file}")


if __name__ == '__main__':
    folder = "../polygon_files/"
    correct_polygon_files_in_folder(folder)

