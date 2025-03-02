from datetime import datetime, timezone, timedelta
import pandas as pd


def formatted_current_time():
    # Получаем текущее время в UTC
    current_time = datetime.now(timezone.utc)

    # Форматируем время в требуемом формате
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return formatted_time

def formatted_start_time(last_days: int = 1, last_hours: int = 0):
    current_time = datetime.now(timezone.utc)
    start_time = current_time - timedelta(days=last_days, hours=last_hours)
    formatted_time = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return formatted_time

def get_coords_filename():
    current_time = datetime.now(timezone.utc)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M')
    return formatted_time

def reformat_df_date(df):
    # Преобразуем столбцы с датами в формат datetime
    df['OriginDate'] = pd.to_datetime(df['OriginDate'])
    df['PublicationDate'] = pd.to_datetime(df['PublicationDate'])
    df['ModificationDate'] = pd.to_datetime(df['ModificationDate'])

    # Форматируем даты в более наглядный вид
    df['OriginDate'] = df['OriginDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['PublicationDate'] = df['PublicationDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    df['ModificationDate'] = df['ModificationDate'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Обрабатываем столбец ContentDate
    df['ContentDate'] = df['ContentDate'].apply(
        lambda
            x: f"{pd.to_datetime(x['Start']).strftime('%Y-%m-%d %H:%M:%S')}" #- {pd.to_datetime(x['End']).strftime('%Y-%m-%d %H:%M:%S')}
    )
    return df


def calculate_date_difference(date1, date2):
    """
    Функция для расчета разницы между двумя датами в днях.

    :param date1: Первая дата (в формате 'YYYY-MM-DD')
    :param date2: Вторая дата (в формате 'YYYY-MM-DD')
    :return: Разница между датами в днях
    """
    try:
        # Преобразуем строки в объекты datetime
        date_format = "%Y-%m-%d"
        d1 = datetime.strptime(date1, date_format)
        d2 = datetime.strptime(date2, date_format)

        # Вычисляем разницу между датами
        difference = abs((d2 - d1).days)  # Используем abs() для получения положительной разницы
        return difference
    except ValueError as e:
        return f"Ошибка: Неверный формат даты. Пожалуйста, используйте формат 'YYYY-MM-DD'. Подробности: {e}"