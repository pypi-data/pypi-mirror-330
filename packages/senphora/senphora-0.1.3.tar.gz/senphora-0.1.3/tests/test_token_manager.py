import pytest
from pathlib import Path
from senphora.loader.token_manager import TokenManager
from dotenv import load_dotenv
import os
import requests_mock

@pytest.fixture
def env_path(tmp_path):
    """Фикстура для создания временного .env файла."""
    env_path = tmp_path / ".test.env"
    with open(env_path, "w") as f:
        f.write("TOKEN_URL=https://example.com/token\n")
        f.write("USERNAME_COPERNICUS=test_user\n")
        f.write("PASSWORD_COPERNICUS=test_password\n")
    return env_path

@pytest.fixture
def token_manager(env_path):
    """Фикстура для создания экземпляра TokenManager."""
    return TokenManager(env_path)

def test_load_env(token_manager):
    """Тест загрузки переменных окружения."""
    token_manager.load_env()
    assert token_manager.url == "https://example.com/token"
    assert token_manager.username == "test_user"
    assert token_manager.password == "test_password"

def test_get_tokens(token_manager, env_path):
    """Тест получения токенов."""
    with requests_mock.Mocker() as m:
        m.post(
            "https://example.com/token",
            json={"access_token": "test_access_token", "refresh_token": "test_refresh_token"},
            status_code=200,
        )

        access_token = token_manager.get_tokens()
        assert access_token == "test_access_token"

        # Проверяем, что токены записаны в .env файл
        load_dotenv(env_path)
        assert os.getenv("ACCESS_TOKEN") == "test_access_token"
        assert os.getenv("REFRESH_TOKEN") == "test_refresh_token"

def test_check_access_token(token_manager, env_path):
    """Тест проверки действительности access_token."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
            status_code=200,
        )

        # Устанавливаем ACCESS_TOKEN в .env файл
        with open(env_path, "a") as f:
            f.write("ACCESS_TOKEN=test_access_token\n")

        assert token_manager.check_access_token()

def test_get_valid_access_token(token_manager, env_path):
    """Тест получения действительного access_token."""
    with requests_mock.Mocker() as m:
        m.get(
            "https://catalogue.dataspace.copernicus.eu/odata/v1/Products",
            status_code=401,  # Токен недействителен
        )
        m.post(
            "https://example.com/token",
            json={"access_token": "new_access_token"},
            status_code=200,
        )

        # Устанавливаем REFRESH_TOKEN в .env файл
        with open(env_path, "a") as f:
            f.write("REFRESH_TOKEN=test_refresh_token\n")

        access_token = token_manager.get_valid_access_token()
        assert access_token == "new_access_token"