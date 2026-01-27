class CustomException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class IncorectData(CustomException):
    detail = "Неверные данные"

class IncorectDate(IncorectData):
    detail = "Неверная дата"

class IncorectPhone(IncorectData):
    detail = "Неверный формат телефона"

class IncorectName(IncorectData):
    detail = 'Длина имени должна быть больше одно'

class MultipleResult(CustomException):
    detail = "Ожидалось получить одну строчку, но было найдено множество."

class UniqueError(CustomException):
    detail = "Объект уже существует"

class ClientUniqueError(UniqueError):
    detail = "Клиент уже существует."

class ClientListUniqueError(UniqueError):
    detail = "Вы уже записаны на приём у данного мастера, на указанную дату."

class UserUniqueError(UniqueError):
    detail = "Пользователь уже существует."


class NoFound(CustomException):
    detail = "Объект не найден"

class ClientNoFound(NoFound):
    detail = "Клиент не найден"

class IdSpecializationNoFound(NoFound):
    detail = "Специализация не найдена."

class MasterNoFound(NoFound):
    detail = "Мастер не найден."


class ApplicationNoFound(NoFound):
    detail = "Заявка не найдена."

class UserNoFound(NoFound):
    detail = "Пользователь не найден."

class ServiceNoFound(NoFound):
    detail = "Услуга не найдена."

class ApplicationApproved(CustomException):
    detail = "Заявка подтверждена"

class IncorectToken(IncorectData):
    detail = "Неверный токен"


class TokenTimeIsOver(CustomException):
    detail = "Время токена вышло"


class TokenDublicate(CustomException):
    detail = "Функция принимает только один токен!"


class RequestCooldownError(CustomException):
    detail = "Действие соверешенно в короткий период"


class CancleRequestAndColldownError(RequestCooldownError):
    detail = (
        "Заявка отклонена, вы можете отправить заявку через 3 дня после предыдущей."
    )


class MasterRequestCooldownError(RequestCooldownError):
    detail = "Найдена активная заявка,вы можете отправить заявку через 3 дня после предыдущей."


class MasterRequestUniqueError(UniqueError):
    detail = "Вы уже мастер."


class MasterRequestAlreadyInProgressError(UniqueError):
    detail = "Вы уже отправили заявку. Дождитесь обработки текущей."


class RoleNotAllowedError(CustomException):
    detail = "Не подходящая роль"
