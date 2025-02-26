from typing import List

from api.dependencies import get_exists_advertiser, get_exists_campaign
from fastapi import APIRouter, Depends
from infra.database.models import Advertiser, Campaign
from schemas.stats import DailyStats, Stats
from services import StatsService

router = APIRouter(prefix='/stats', tags=['Statistics'])


@router.get('/campaigns/{campaign_id}', response_model=Stats)
async def get_campaign_stats(
    campaign: Campaign = Depends(get_exists_campaign),
    service: StatsService = Depends(StatsService)
):
    stats = await service.get_campaign_stats(campaign_id=campaign.id)

    return stats


@router.get('/advertisers/{advertiser_id}/campaigns', response_model=Stats)
async def get_advertiser_campaigns_stats(
    advertiser: Advertiser = Depends(get_exists_advertiser),
    service: StatsService = Depends(StatsService)
):
    stats = await service.get_advertiser_stats(advertiser.id)

    return stats


@router.get('/campaigns/{campaign_id}/daily', response_model=List[DailyStats])
async def get_campaign_daily_stats(
    campaign: Campaign = Depends(get_exists_campaign),
    service: StatsService = Depends(StatsService)
):
    stats = await service.get_campaign_daily_stats(campaign_id=campaign.id)

    return stats


@router.get('/advertisers/{advertiser_id}/campaigns/daily', response_model=List[DailyStats])
async def get_advertiser_campaigns_daily_stats(
    advertiser: Advertiser = Depends(get_exists_advertiser),
    service: StatsService = Depends(StatsService)
):
    stats = await service.get_advertiser_daily_stats(advertiser_id=advertiser.id)

    return stats
