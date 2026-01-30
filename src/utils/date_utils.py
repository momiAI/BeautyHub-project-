from datetime import datetime,timezone

from src.utils.exceptions import UserUpdateCooldownError


class DateUtils: 
    
    @property
    def now(self):
        return datetime.now(timezone.utc)

    def check_last_update(self, date_bd : datetime):
        hours = (datetime.now(timezone.utc) - date_bd).total_seconds() / 3600
        if hours < 24:
            raise UserUpdateCooldownError
        

date_utils = DateUtils()