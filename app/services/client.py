from typing import List

from infra.database.models import Client
from infra.repository import ClientRepository


class ClientService:
    def __init__(self):
        self.repo = ClientRepository()

    async def bulk(self, data: list[dict]) -> List[Client]:
        return await self.repo.bulk_clients(data)
