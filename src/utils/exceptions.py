class CustomException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class IncorectData(CustomException):
    detail = "Неверные данные"


class IncorectPhone(IncorectData):
    detail = "Неверный формат телефона"


class UniqueError(CustomException):
    detail = "Объект уже существует"

class UserUniqueError(UniqueError):
    detail = "Пользователь уже существует."

class NoFound(CustomException):
    detail = "Объект не найден"

class UserNoFound(NoFound):
    detail = "Пользователь не найден."