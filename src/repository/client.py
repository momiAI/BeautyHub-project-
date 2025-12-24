from src.repository.base import BaseOrmRep
from src.models.client import ClientModel,ClientRatingModel
from src.schemas.client import ClientSchema,ClientRatingRelationSchema


class ClientRepository(BaseOrmRep):
    model = ClientModel
    schema = ClientSchema


class ClientRatingRelationRepository(BaseOrmRep):
    model = ClientRatingModel
    schema = ClientRatingRelationSchema