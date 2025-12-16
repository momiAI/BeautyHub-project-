from pydantic import BaseModel
from datetime import date


class DayOffSchema(BaseModel):
    id: int
    id_master: int
    day: date
    reason: str | None
