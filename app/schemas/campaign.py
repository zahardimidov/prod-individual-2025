from typing import List, Optional, Self

from infra.database.models import Campaign
from pydantic import BaseModel, Field, model_validator
from schemas._base import (IgnoreCaseEnum, NonEmptyStr, NonNegativeFloat,
                           NonNegativeInt, RequestModel, Age)


class CampaignTargetGenderEnum(IgnoreCaseEnum):
    male = 'MALE'
    female = 'FEMALE'
    all = 'ALL'


class CampaignTargeting(RequestModel):
    gender: Optional[CampaignTargetGenderEnum] = None
    age_from: Optional[Age] = None
    age_to: Optional[Age] = None
    location: Optional[NonEmptyStr] = None

    @model_validator(mode='after')
    def full_validation(self) -> Self:
        if self.age_from and self.age_to and self.age_from > self.age_to:
            raise ValueError(
                'Значение параметра age_from не может превышать значение параметра age_to')
        return self


class CampaignBase(BaseModel):
    impressions_limit: NonNegativeInt
    clicks_limit: NonNegativeInt
    cost_per_impression: NonNegativeFloat
    cost_per_click: NonNegativeFloat
    ad_title: NonEmptyStr
    ad_text: NonEmptyStr
    start_date: NonNegativeInt
    end_date: NonNegativeInt

    targeting: Optional[CampaignTargeting] = None

    @model_validator(mode='after')
    def full_validation(self) -> Self:
        if self.start_date > self.end_date:
            raise ValueError(
                'Значение параметра start_date не может превышать значение параметра end_date')
        if self.clicks_limit > self.impressions_limit:
            raise ValueError(
                'Значение параметра clicks_limit не может превышать значение параметра impressions_limit')
        return self


class CampaignRequest(CampaignBase, RequestModel):
    ...


class CampaignResponse(CampaignBase):
    campaign_id: NonEmptyStr
    advertiser_id: NonEmptyStr
    images: List[str] = Field(default_factory=list)

    @classmethod
    def from_object(cls, campaign: Campaign):
        data = dict(
            campaign_id=campaign.id,
            advertiser_id=campaign.advertiser_id,
            impressions_limit=campaign.impressions_limit,
            clicks_limit=campaign.clicks_limit,
            cost_per_impression=campaign.cost_per_impression,
            cost_per_click=campaign.cost_per_click,
            ad_title=campaign.ad_title,
            ad_text=campaign.ad_text,
            start_date=campaign.start_date,
            end_date=campaign.end_date,
            targeting=CampaignTargeting(
                gender=campaign.gender,
                age_from=campaign.age_from,
                age_to=campaign.age_to,
                location=campaign.location
            ),
            images=campaign.images
        )
        return cls(**data)
