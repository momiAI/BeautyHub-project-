from datetime import datetime,timezone,timedelta

from src.utils.exceptions import UserUpdateCooldownError


class DateUtils: 
    
    @property
    def now(self):
        return datetime.now(timezone.utc)
    
    @property
    def create_expire_token(self) -> datetime:
        return self.now + timedelta(minutes=3)

    def check_last_update(self, date_bd : datetime):
        hours = (datetime.now(timezone.utc) - date_bd).total_seconds() / 3600
        if hours < 24:
            raise UserUpdateCooldownError
    
    def check_last_atempt(self,last_attemp : datetime) -> bool:
        return True if (self.now - last_attemp).total_seconds() > 3 else False
        
        

date_utils = DateUtils()