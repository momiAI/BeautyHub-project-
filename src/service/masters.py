

from src.service.base import BaseService
from src.schemas.masters import MasterCreateRequestSchema
from src.utils.masters_utils import master_utils
from src.utils.exceptions import MasterRequestAlreadyInProgressError, MasterRequestCooldownError,MasterRequestUniqueError,CancleRequestAndColldownError,NoFound

class MastersService(BaseService):

    async def request_application(self, id_user : int, data : MasterCreateRequestSchema ):
        data_update = master_utils.converts_request_data(id_user,data)
        try:
            application = await self.db.master_request.get_object(id_user = id_user)
            if application:
                obj = master_utils.check_application(application)
                return await self.db.master_request.update(id = obj.id,values=data_update)
        except MasterRequestCooldownError:
            raise MasterRequestCooldownError
        except MasterRequestUniqueError:
            raise MasterRequestUniqueError
        except CancleRequestAndColldownError:
            raise CancleRequestAndColldownError
        except MasterRequestAlreadyInProgressError:
            raise MasterRequestAlreadyInProgressError
        except NoFound:
            pass

        return await self.db.master_request.create(data_update)
        