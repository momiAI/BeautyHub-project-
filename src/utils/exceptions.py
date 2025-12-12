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

class IncorectToken(IncorectData):
    detail = "Неверный токен"

class TokenTimeIsOver(CustomException):
    detail = "Время токена вышло"

class TokenDublicate(CustomException):
    detail = "Функция принимает только один токен!"

class RequestCooldownError(CustomException):
    detail = "Действие соверешенно в короткий период"

class CancleRequestAndColldownError(RequestCooldownError):
    detail = "Заявка отклонена, вы можете отправить заявку через 3 дня после предыдущей."

class MasterRequestCooldownError(RequestCooldownError):
    detail = "Найдена активная заявка,вы можете отправить заявку через 3 дня после предыдущей."

class MasterRequestUniqueError(UniqueError):
    detail = "Вы уже мастер."

class MasterRequestAlreadyInProgressError(UniqueError):
    detail = "Вы уже отправили заявку. Дождитесь обработки текущей."