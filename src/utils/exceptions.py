class CustomException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class IncorectData(CustomException):
    detail = "Неверные данные"

class IncorectTypeFile(IncorectData):
    detail = "Неверный формат файла"

class IncorectTypeImage(IncorectTypeFile):
    detail = "Данный формат изображения не поддерживается."

class IncorectDate(IncorectData):
    detail = "Неверная дата"

class IncorectNowPassword(IncorectData):
    detail = "Неверный текущий пароль"

class IncorectPhone(IncorectData):
    detail = "Неверный формат телефона"

class IncorectName(IncorectData):
    detail = 'Длина имени должна быть больше одно'

class MultipleResult(CustomException):
    detail = "Ожидалось получить одну строчку, но было найдено множество."

class UniqueError(CustomException):
    detail = "Объект уже существует"

class PasswordDuplicate(UniqueError):
    detail = "Новый пароль должен отличаться от старого."

class ClientUniqueError(UniqueError):
    detail = "Клиент уже существует."

class ClientListUniqueError(UniqueError):
    detail = "Вы уже записаны на приём у данного мастера, на указанную дату."

class UserUniqueError(UniqueError):
    detail = "Пользователь уже существует."


class NoFound(CustomException):
    detail = "Объект не найден"

class SalonNoFound(NoFound):
    detail = "Салон не найден"

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

class UserUpdateCooldownError(RequestCooldownError):
    detail = "Обновить свои данные можно 1 раз в 24 часа."

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

class PasswordNotMatch(CustomException):
    detail = 'Пароли не совпадают.'
