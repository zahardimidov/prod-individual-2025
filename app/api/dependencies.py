from fastapi import Depends, HTTPException
from infra.database.models import Advertiser
from services.advertisers import AdvertiserService
from services.campaign import CampaignService
from services.client import ClientService


async def get_exists_client(client_id: str, service: ClientService = Depends(ClientService)):
    client = await service.repo.get(id=client_id)

    if not client:
        raise HTTPException(status_code=404, detail='Клиент не найден')

    return client


async def get_exists_advertiser(advertiser_id: str, service: AdvertiserService = Depends(AdvertiserService)):
    advertiser = await service.repo.get(id=advertiser_id)

    if not advertiser:
        raise HTTPException(status_code=404, detail='Рекламодатель не найден')

    return advertiser


async def get_advertiser_exists_campaign(
        campaign_id: str,
        advertiser: Advertiser = Depends(get_exists_advertiser),
        service: CampaignService = Depends(CampaignService)):

    campaign = await service.get_campaign(advertiser_id=advertiser.id, campaign_id=campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=404, detail='Рекламная кампания не найдена')

    return campaign


async def get_exists_campaign(
        campaign_id: str,
        service: CampaignService = Depends(CampaignService)):

    campaign = await service.repo.get(campaign_id)

    if not campaign:
        raise HTTPException(
            status_code=404, detail='Рекламная кампания не найдена')

    return campaign
