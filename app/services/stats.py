from infra.repository import AdvertiserRepository, CampaignRepository
from services import TimeAdvanceService
from schemas.stats import DailyStats, Stats

class StatsService:
    def __init__(self):
        self.advertisers = AdvertiserRepository()
        self.campaigns = CampaignRepository()

    async def get_campaign_stats(self, campaign_id: str):
        stats = await self.campaigns.stats(campaign_id)

        return Stats(**stats).model_dump()

    async def get_advertiser_stats(self, advertiser_id: str):
        stats = await self.advertisers.stats(advertiser_id)
        
        return Stats(**stats).model_dump()
    
    async def get_campaign_daily_stats(self, campaign_id: str):
        campaign = await self.campaigns.get(campaign_id)

        stats = []
        current_date = await TimeAdvanceService().get_date()
        end = min(campaign.end_date, current_date)

        for date in range(end, campaign.start_date - 1, -1):
            stat = await self.campaigns.daily_stats(campaign_id, date)
            stats.append(DailyStats(date=date, **stat).model_dump())
            
        return stats

    async def get_advertiser_daily_stats(self, advertiser_id: str):
        stats = []
        current_date = await TimeAdvanceService().get_date()
        
        for date in range(current_date, -1, -1):
            stat = await self.advertisers.daily_stats(advertiser_id, date)
            stats.append(DailyStats(date=date, **stat).model_dump())
            
        return stats

