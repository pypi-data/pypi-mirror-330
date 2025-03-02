class NotUpdateToken(Exception):
    def __init__(self, message = 'Не удалось обновить токен'):
        self.message = message
        super().__init__(self.message)

class ProductNotFoundError(Exception):
    def __init__(self, message = 'Не удалось найти файл'):
        self.message = message
        super().__init__(self.message)

class ProductNotLoadedError(Exception):
    def __init__(self, message = 'Не удалось скачать файл'):
        self.message = message
        super().__init__(self.message)

class TooManyFoldersError(Exception):
    def __init__(self, message = "Найдено слишком много папок"):
        self.message = message
        super().__init__(self.message)