from setuptools import setup, find_packages

setup(
    name="senphora",  # Имя вашей библиотеки
    version="0.2.0.0",  # Версия
    packages=find_packages(where="src"),  # Автоматически находит все пакеты
    package_dir={"": "src"},
    install_requires=[
        "python-dotenv>=1.0.1",
        "requests>=2.32.3",
        "pandas>=2.2.3",
        "tqdm>=4.67.1",
        "rasterio>=1.4.3",
        "pyproj>=3.7.1",
        "shapely>=2.0.7",
        "pillow>=11.1.0",
        "loguru==0.7.3"
    ],  # Зависимости (если есть)
    author="Babahasko",
    author_email="zakutni4ek@gmail.com",
    description="Senphora Python library for working with sentinel API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.12",
)
