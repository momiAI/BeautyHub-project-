from enum import Enum

class CategoryEnum(Enum):
    FACE = 'face'
    HAIR = 'hair' 
    NAILS = 'nails' 
    LASH = 'lash' 
    BROWS = 'brows'
    DEPILATION = 'depilation'


class UserRoleEnum(Enum):
    ADMIN = 'admin' 
    MASTER = 'master' 
    CLIENT = 'client'


class ReceptionStatusEnum(Enum):
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


class WeekDay(Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"