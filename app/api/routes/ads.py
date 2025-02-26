from fastapi import APIRouter, Depends, Response, Query
from services import CampaignService, ClientService
from schemas.ads import CampaignForClient
from api.dependencies import get_exists_client

router = APIRouter(prefix='/ads', tags=['Ads'])


@router.get('', response_model=CampaignForClient)
async def get_ad(
    client_id = Query(..., min_length=1),
    campaigns: CampaignService = Depends(CampaignService),
    clients: ClientService = Depends(ClientService)
):
    client = await get_exists_client(client_id, clients)
    campaign = await campaigns.get_relevant_campaign(client)

    return CampaignForClient.from_object(campaign)



@router.post('/{ad_id}/click')
async def click_ad(
    ad_id: str,
    client_id = Query(..., min_length=1),
    campaigns: CampaignService = Depends(CampaignService),
    clients: ClientService = Depends(ClientService)
):
    client = await get_exists_client(client_id, clients)
    await campaigns.click_campaign(client, ad_id)
    
    return Response(status_code=204)
