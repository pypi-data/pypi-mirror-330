import os
import sys
import requests
from dotenv import load_dotenv
from pathlib import Path


class TokenManager:
    def __init__(self, env_path:Path = ".env"):
        """
        Инициализация менеджера токенов.
        :param env_path: Путь к .env файлу.
        """
        self.env_path = env_path
        self.load_env()
        self.url = os.getenv("TOKEN_URL")
        self.username = os.getenv("USERNAME_COPERNICUS")
        self.password = os.getenv("PASSWORD_COPERNICUS")
        self.client_id = "cdse-public"

    def load_env(self):
        """
        Загрузка переменных окружения из .env файла.
        """
        if not os.path.exists(self.env_path):
            raise FileNotFoundError(f"Файл {self.env_path} не найден.")
        load_dotenv(self.env_path)

    def get_tokens(self):
        """
        Получение access_token и refresh_token через аутентификацию.
        """
        data = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.url, data=data, headers=headers)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            self.save_tokens(access_token, refresh_token)
            print("Токены успешно получены и сохранены.")
            return access_token
        else:
            print(f"Ошибка Аутентификации. Status Code: {response.status_code}. Response: {response.text}")
            sys.exit(1)

    def save_tokens(self, access_token, refresh_token):
        """
        Сохранение токенов в .env файл.
        """
        env_vars = {}
        if os.path.exists(self.env_path):
            with open(self.env_path, "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        env_vars[key] = value

        env_vars["ACCESS_TOKEN"] = str(access_token)
        env_vars["REFRESH_TOKEN"] = str(refresh_token)

        with open(self.env_path, "w") as file:
            for key, value in env_vars.items():
                file.write(f"{key}={value}\n")
        print(f"Токены успешно записаны в {self.env_path} файл.")

    def refresh_access_token(self):
        """
        Обновление access_token через refresh_token.
        """
        refresh_token = os.getenv("REFRESH_TOKEN")
        if not refresh_token:
            print("REFRESH_TOKEN не найден. Требуется переаутентификация.")
            return self.get_tokens()

        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(self.url, data=data, headers=headers)

        if response.status_code == 200:
            new_access_token = response.json().get("access_token")
            self.save_tokens(new_access_token, refresh_token)  # Сохраняем только новый access_token
            print("ACCESS_TOKEN успешно обновлен.")
            self.load_env()
            return new_access_token
        else:
            print(f"Не удалось обновить ACCESS_TOKEN через REFRESH_TOKEN. Требуется переаутентификация."
                  f" Status Code: {response.status_code} Response:, {response.text}")
            return self.get_tokens()  # Переаутентификация, если refresh_token устарел

    def check_access_token(self):
        """
        Проверка работоспособности access_token.
        """
        access_token = os.getenv("ACCESS_TOKEN")
        if not access_token:
            print("ACCESS_TOKEN не найден. Требуется аутентификация.")
            return False

        url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return True
        else:
            print("ACCESS_TOKEN недействителен. Требуется обновление.")
            return False

    def get_valid_access_token(self):
        """
        Получение действительного access_token.
        """
        if self.check_access_token():
            print("ACCESS_TOKEN действителен")
            return os.getenv("ACCESS_TOKEN")
        else:
            print("Обновляем ACCESS_TOKEN...")
            return self.refresh_access_token()