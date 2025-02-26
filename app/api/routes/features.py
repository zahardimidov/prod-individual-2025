from fastapi import APIRouter, Depends, HTTPException, Response
from schemas.features import *
from services import ModerationService, YandexCloudService

router = APIRouter(prefix='/text', tags=['Features'])


@router.post('/generate', response_model=GenerateTextResponse)
async def generate_text(data: GenerateText, service: YandexCloudService = Depends(YandexCloudService)):
    text = await service.generate_text(advertiser_name=data.advertiser_name, ad_name=data.ad_title)

    if not text:
        raise HTTPException(status_code=400, detail='Что-то пошло не так')

    return dict(text=text)


@router.post('/moderation/check', response_model=TextCheckResponse)
async def text_moderation_check(data: Text, service: ModerationService = Depends(ModerationService)):
    toxicity = await service.check_text(text=data.text)

    return dict(toxicity=toxicity)


@router.post('/moderation/rate')
async def set_text_moderation_rate(data: ModerationRate, service: ModerationService = Depends(ModerationService)):
    await service.set_rate(data.rate)

    return Response(status_code=200)


@router.post('/moderation/validate', response_model=TextModerationResponse)
async def moderation_validate(data: Text, service: ModerationService = Depends(ModerationService)):
    if await service.validate_text(data.text):
        return TextModerationResponse(is_valid=True)
    return TextModerationResponse(is_valid=False)
