from typing import List

from infra.database.models import Advertiser
from infra.repository import AdvertiserRepository, MLScoreRepository


class AdvertiserService:
    def __init__(self):
        self.repo = AdvertiserRepository()
        self.ml_score = MLScoreRepository()

    async def bulk(self, data: list[dict]) -> List[Advertiser]:
        return await self.repo.bulk_advertisers(data)

    async def set_ml_score(self, client_id: str, advertiser_id: str, score: int):
        return await self.ml_score.create(client_id=client_id, advertiser_id=advertiser_id, score=score)