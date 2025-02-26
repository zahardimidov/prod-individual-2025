from infra.database.models import Advertiser
from schemas._base import BaseModel, RequestModel, NonEmptyStr, NonNegativeInt


class AdvertiserResponse(BaseModel):
    advertiser_id: NonEmptyStr
    name: NonEmptyStr

    @classmethod
    def from_object(cls, advertiser: Advertiser):
        return cls(advertiser_id=advertiser.id, name=advertiser.name)


class AdvertiserRequest(AdvertiserResponse, RequestModel):
    ...


class MLScoreRequest(RequestModel):
    client_id: NonEmptyStr
    advertiser_id: NonEmptyStr
    score: NonNegativeInt
