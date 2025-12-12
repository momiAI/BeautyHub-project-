from src.repository.base import BaseRep
from src.models.master import MasterModel,MasterRequestModel
from src.schemas.masters import MasterSchema,MasterRequestSchema

class MasterRepository(BaseRep):
    model = MasterModel
    schema = MasterSchema





class MasterRequestRepository(BaseRep):
    model = MasterRequestModel
    schema = MasterRequestSchema