from pydantic import BaseModel
from datetime import date


class DayOffCreateSchema(BaseModel):
    day: date
    reason: str | None = None

class DayOffDBSchema(DayOffCreateSchema):
    id_master: int

class DayOffSchema(DayOffDBSchema):
    id: int