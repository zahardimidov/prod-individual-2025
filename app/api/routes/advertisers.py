from typing import List

from api.dependencies import get_exists_advertiser, get_exists_client
from fastapi import APIRouter, Depends, Response
from infra.database.models import Advertiser
from schemas.advertiser import (AdvertiserRequest, AdvertiserResponse,
                                MLScoreRequest)
from services import AdvertiserService, ClientService

router = APIRouter(prefix='', tags=['Advertisers'])


@router.get('/advertisers/{advertiser_id}', response_model=AdvertiserResponse, status_code=200)
async def get_advertiser(
    advertiser: Advertiser = Depends(get_exists_advertiser)
):
    return AdvertiserResponse.from_object(advertiser)


@router.post('/advertisers/bulk', response_model=List[AdvertiserResponse], status_code=201)
async def bulk_advertisers(
    advertisers: List[AdvertiserRequest],
    service: AdvertiserService = Depends(AdvertiserService)
):
    items = await service.bulk([advertiser.model_dump() for advertiser in advertisers])

    return [
        AdvertiserResponse.from_object(advertiser) for advertiser in items
    ]


@router.post('/ml-scores')
async def ml_scores(
    ml: MLScoreRequest,
    advertisers: AdvertiserService = Depends(AdvertiserService),
    clients: ClientService = Depends(ClientService)
):
    advertiser = await get_exists_advertiser(ml.advertiser_id, advertisers)
    client = await get_exists_client(ml.client_id, clients)

    await advertisers.set_ml_score(client_id=client.id, advertiser_id=advertiser.id, score=ml.score)

    return Response(status_code=200)
