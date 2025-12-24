from src.repository.users import UsersRepository
from src.repository.master import (
    MasterRepository,
    MasterRequestRepository,
    WorkDayRepository,
    DayOffRepository,
    SpecializationMasterRelationRepository,
    MasterSpecializationRepository
)
from src.repository.service import ServiceRepository,ServiceRelationMasterRepository
from src.repository.reception import ReceptionRepository
from src.repository.client import ClientRepository,ClientRatingRelationRepository


class DbManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UsersRepository(self.session)

        self.client = ClientRepository(self.session)
        self.client_rating = ClientRatingRelationRepository(self.session)

        self.master = MasterRepository(self.session)
        self.master_request = MasterRequestRepository(self.session)
        self.workday = WorkDayRepository(self.session)
        self.dayoff = DayOffRepository(self.session)
        self.master_specialization = MasterSpecializationRepository(self.session)
        self.master_specialization_relation = SpecializationMasterRelationRepository(self.session)
    

        self.service = ServiceRepository(self.session)
        self.service_relation = ServiceRelationMasterRepository(self.session)

        self.reception = ReceptionRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
