from src.repository.users import UsersRepository
from src.repository.master import MasterRepository,MasterRequestRepository


class DbManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UsersRepository(self.session)
        self.master = MasterRepository(self.session)
        self.master_request = MasterRequestRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
