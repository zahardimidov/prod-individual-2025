from exceptions import ServiceException
from infra.repository import (CampaignRepository, ClickRepository, Client,
                              ImpressionRepository)
from infra.s3.storage import Storage
from schemas.campaign import CampaignRequest, CampaignTargeting

from .time import TimeAdvanceService


class CampaignService:
    def __init__(self):
        self.repo = CampaignRepository()
        self.impressions = ImpressionRepository()
        self.clicks = ClickRepository()

        self.time_service = TimeAdvanceService()


    async def validate_campaign_dates(self, data: dict):
        current_date = await self.time_service.get_date()

        if data.get('start_date') is not None and data.get('start_date') < current_date:
            raise ServiceException(
                status_code=400, detail='Дата начала действия кампании не может быть в прошлом')

        if data.get('end_date') is not None and data.get('end_date') < current_date:
            raise ServiceException(
                status_code=400, detail='Дата окончания действия кампании не может быть в прошлом')

        if data.get('start_date') is not None and data.get('end_date') is not None and data.get('start_date') > data.get('end_date'):
            raise ServiceException(
                status_code=400, detail='Кампания не может закончиться, не начавшись')

    async def create_campaign(self, advertiser_id: str, data: dict):
        await self.validate_campaign_dates(data=data)

        return await self.repo.create(advertiser_id=advertiser_id, **data)

    async def get_campaigns_page(self, advertiser_id: str, size: int, page: int):
        limit = size
        offset = (page - 1) * size

        return await self.repo.find(limit=limit, offset=offset, advertiser_id=advertiser_id)

    async def get_campaign(self, advertiser_id: str, campaign_id: str):
        campaign = await self.repo.find_one(id=campaign_id, advertiser_id=advertiser_id)

        return campaign

    async def update_campaign(self, campaign_id: str, data: dict):
        campaign = await self.repo.find_one(id=campaign_id)

        current_date = await self.time_service.get_date()

        if campaign.start_date <= current_date:
            if data.get('impressions_limit') != campaign.impressions_limit:
                raise ServiceException(
                    status_code=400, detail='Вы не можете изменить количество показов. Рекламная кампания уже началась')

            if data.get('clicks_limit') != campaign.clicks_limit:
                raise ServiceException(
                    status_code=400, detail='Вы не можете изменить количество переходов по объявлению. Рекламная кампания уже началась')

            if data.get('start_date') != campaign.start_date:
                raise ServiceException(
                    status_code=400, detail='Вы не можете изменить дату начала действия кампании. Рекламная кампания уже началась')

            if data.get('end_date') != campaign.end_date:
                raise ServiceException(
                    status_code=400, detail='Вы не можете изменить дату окончания действия кампании. Рекламная кампания уже началась')

        await self.validate_campaign_dates(data)

        return await self.repo.update(id=campaign.id, **data)

    async def remove_campaign(self, campaign_id: str):
        await self.repo.delete(id=campaign_id)

    async def update_campaign_images(self, campaign_id: str, images: list[bytes]):
        storage = Storage('images')
        campaign = await self.repo.get(campaign_id)

        for ind in range(1, campaign.image_count + 1):
            filename = f'{campaign_id}_{ind}.png'
            await storage.delete_file(filename)

        for ind, image in enumerate(images, start=1):
            filename = f'{campaign_id}_{ind}.png'
            await storage.upload_file(image, filename)

        return await self.repo.update(campaign_id, image_count=len(images))

    def parse_request_data(self, data: dict):
        update_data = {}
        for k in CampaignRequest.model_fields.keys():
            if k == 'targeting':
                continue
            update_data[k] = None
        for k in CampaignTargeting.model_fields.keys():
            update_data[k] = None
        for k, v in data.items():
            if k in update_data:
                update_data[k] = v
        if data.get('targeting') is not None:
            update_data.update(dict(data['targeting']))
        return update_data

    async def get_relevant_campaign(self, client: Client):
        current_date = await self.time_service.get_date()

        campaign = await self.repo.get_relevant_campaign(client, current_date)

        if not campaign:
            raise ServiceException(
                status_code=404, detail='Не найдена ни одна подходящая реклама')

        impression = await self.impressions.find_one(client_id=client.id, campaign_id=campaign.id)
        if not impression:
            impression = await self.impressions.create(client_id=client.id, campaign_id=campaign.id, date=current_date, cost=campaign.cost_per_impression)

        return campaign

    async def click_campaign(self, client: Client, campaign_id: str):
        campaign = await self.repo.get(campaign_id)

        if not campaign:
            raise ServiceException(
                status_code=404, detail='Реклама не найдена')
        
        current_date = await self.time_service.get_date()

        impression = await self.impressions.find_one(client_id=client.id, campaign_id=campaign.id)
        if not impression:
            print('impression')
            impression = await self.impressions.create(client_id=client.id, campaign_id=campaign.id, date=current_date, cost=campaign.cost_per_impression)

        click = await self.clicks.find_one(client_id=client.id, campaign_id=campaign.id)
        if not click:
            print('click')
            click = await self.clicks.create(client_id=client.id, campaign_id=campaign.id, date=current_date, cost=campaign.cost_per_click)
