class NotUpdateToken(Exception):
    def __init__(self, message = 'Не удалось обновить токен'):
        self.message = message
        super().__init__(self.message)

class NotFoundError(Exception):
    def __init__(self, message = 'Не удалось скачать файл'):
        self.message = message
        super().__init__(self.message)