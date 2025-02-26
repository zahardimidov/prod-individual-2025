from typing import List, Union, Any

from api.dependencies import (get_advertiser_exists_campaign,
                              get_exists_advertiser)
from fastapi import APIRouter, Depends, Query, Response, UploadFile, HTTPException
from infra.database.models import Advertiser, Campaign
from schemas.campaign import CampaignRequest, CampaignResponse
from services import CampaignService, ModerationService

router = APIRouter(
    prefix='/advertisers/{advertiser_id}/campaigns', tags=['Campaigns'])


@router.post('', response_model=CampaignResponse, status_code=201)
async def create_campaign(
    data: CampaignRequest,
    advertiser: Advertiser = Depends(get_exists_advertiser),
    service: CampaignService = Depends(CampaignService),
    moderation: ModerationService = Depends(ModerationService)
):
    await moderation.validate_text(data.ad_title, strict=True)
    await moderation.validate_text(data.ad_text, strict=True)

    campaign_data = service.parse_request_data(data.model_dump())
    campaign = await service.create_campaign(advertiser_id=advertiser.id, data=campaign_data)

    return CampaignResponse.from_object(campaign)


@router.get('', response_model=List[CampaignResponse])
async def get_campaigns(
    size: int = Query(default=10, gt=0),
    page: int = Query(default=1, gt=0),
    advertiser: Advertiser = Depends(get_exists_advertiser),
    service: CampaignService = Depends(CampaignService)
):
    campaigns = await service.get_campaigns_page(advertiser_id=advertiser.id, size=size, page=page)

    return [CampaignResponse.from_object(campaign) for campaign in campaigns]


@router.get('/{campaign_id}', response_model=CampaignResponse)
async def get_campaign_by_id(
    campaign: Campaign = Depends(get_advertiser_exists_campaign)
):
    return CampaignResponse.from_object(campaign)


@router.put('/{campaign_id}', response_model=CampaignResponse, status_code=200)
async def update_campaign(
    data: CampaignRequest,
    campaign: Campaign = Depends(get_advertiser_exists_campaign),
    service: CampaignService = Depends(CampaignService),
    moderation: ModerationService = Depends(ModerationService)
):
    await moderation.validate_text(data.ad_title, strict=True)
    await moderation.validate_text(data.ad_text, strict=True)

    update_data = service.parse_request_data(data.model_dump())
    campaign = await service.update_campaign(campaign_id=campaign.id, data=update_data)

    return CampaignResponse.from_object(campaign)


@router.put('/{campaign_id}/upload_images', status_code=200, response_model=CampaignResponse)
async def upload_campaign_images(
    images:  Union[List[UploadFile], List[str]] = [],
    campaign: Campaign = Depends(get_advertiser_exists_campaign),
    service: CampaignService = Depends(CampaignService)
):
    images = [image for image in images if not isinstance(image, str)]

    if len(images) > 10:
        raise HTTPException(status_code=400, detail='Вы можете загрузить до 10 изображений')
    
    b = []
    for image in images:
        if not image.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
            raise HTTPException(status_code=400, detail='Передан недопустимый формат файла')
        b.append(await image.read())

    campaign = await service.update_campaign_images(campaign.id, images=b)

    return CampaignResponse.from_object(campaign)


@router.delete('/{campaign_id}', status_code=204)
async def delete_campaign_by_id(
    campaign: Campaign = Depends(get_advertiser_exists_campaign),
    service: CampaignService = Depends(CampaignService)
):
    await service.remove_campaign(campaign_id=campaign.id)

    return Response(status_code=204)
