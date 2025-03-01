from datetime import datetime

def filter_products_by_l2a(product_dict):
    filtered_products_id = {key: value for key, value in product_dict['Name'].items() if "L2A" in value}
    filtered_indecies = [key for key in filtered_products_id.keys()]

    filtered_products = get_data_by_index(product_dict, filtered_indecies)
    print(f"Число результатов l2a:{len(filtered_products['Name'])}" )
    return filtered_products


def filter_latest_product(product_dict):
    product_dates = product_dict['ContentDate']
    parsed_dates = {
        index: datetime.fromisoformat(value['Start'].rstrip('Z'))
        for index, value in product_dates.items()
    }
    latest_index = [max(parsed_dates, key=parsed_dates.get)]

    latest_product = get_data_by_index(product_dict, latest_index)
    flat_data = get_flat_data(latest_product)
    return flat_data

# Вспомогательная функция для получения всех записей с нужным индексом
def get_data_by_index(data_dict, filtered_indexies):
    filtered_data = {}
    for key_name, value in data_dict.items():
        # print(f'{key_name} : {value}')
        filtered_data_items = {key: value for key, value in data_dict[key_name].items() if key in filtered_indexies}
        filtered_data[key_name] = filtered_data_items
    return filtered_data

def get_flat_data(data):
    # Определяем индекс (предполагаем, что все ключи имеют одинаковый индекс)
    index = next(iter(data.values())).keys().__iter__().__next__()

    # Преобразуем словарь, убирая индекс
    flat_data = {key: value[index] for key, value in data.items()}
    return flat_data