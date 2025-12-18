from pydantic import BaseModel
from datetime import time

from src.models.enum import WeekDayEnum

class WorkDayRequstSchema(BaseModel):
    day_of_week: list[WeekDayEnum]
    start_time: time
    end_time: time

class WorkDayDbSchema(WorkDayRequstSchema):
    id_master: int


class WorkDaySchema(WorkDayDbSchema):
    id: int
    
