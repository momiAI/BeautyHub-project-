from enum import Enum


class CategoryEnum(str, Enum):
    FACE = "face"
    HAIR = "hair"
    NAILS = "nails"
    LASH = "lash"
    BROWS = "brows"
    DEPILATION = "depilation"


class UserRoleEnum(str, Enum):
    ADMIN = "admin"
    MASTER = "master"
    CLIENT = "client"
    ADMINISTRATOR = "administrator"

class ReceptionAdministraotStatusEnum(str,Enum):
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"    
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"
    REFUNDED = "refunded"

class ReceptionStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED_BY_CLIENT = "cancelled_by_client"
    CANCELLED_BY_MASTER = "cancelled_by_master"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"
    AWAITING_PAYMENT = "awaiting_payment"
    REFUNDED = "refunded"


class WeekDayEnum(str, Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class MasterRequestStatusEnum(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_PROGRESS = "in_progress"

class CityEnum(str, Enum):
    moscow = "moscow"
    spb = "spb"
    novosibirsk = "novosibirsk"
    ekaterinburg = "ekaterinburg"
    kazan = "kazan"
    nizhny_novgorod = "nizhny_novgorod"
    chelyabinsk = "chelyabinsk"
    samara = "samara"
    ufa = "ufa"
    rostov_on_don = "rostov_on_don"
    krasnoyarsk = "krasnoyarsk"
    perm = "perm"
    voronezh = "voronezh"
    volgograd = "volgograd"
    krasnodar = "krasnodar"