from pydantic import BaseModel
from datetime import time

from src.models.enum import WeekDayEnum


class WorkDaySchema(BaseModel):
    id: int
    id_master: int
    day_of_week: list[WeekDayEnum]
    start_time: time
    end_time: time
