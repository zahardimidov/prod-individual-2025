from typing import List
from pydantic import BaseModel, Field
from schemas._base import NonEmptyStr, NonNegativeFloat, NonNegativeInt
from infra.database.models import Campaign


class CampaignForClient(BaseModel):
    ad_id: NonEmptyStr
    ad_title: NonEmptyStr
    ad_text: NonEmptyStr
    advertiser_id: NonEmptyStr
    images: List[str] = Field(default_factory=list)

    @classmethod
    def from_object(cls, campaign: Campaign):
        return cls(
            ad_id=campaign.id,
            ad_title=campaign.ad_text,
            ad_text=campaign.ad_text,
            advertiser_id=campaign.advertiser_id,
            images = campaign.images
        )


class RelevantCampaign(BaseModel):
    id: NonEmptyStr

    cost_per_impression: NonNegativeFloat
    cost_per_click: NonNegativeFloat

    clicks_count: NonNegativeInt
    impressions_count: NonNegativeInt

    ml_score: NonNegativeFloat
    normilized_ml_score: NonNegativeFloat
    click_possibility: NonNegativeFloat
    possible_profit: NonNegativeFloat
    normilized_possible_profit: NonNegativeFloat = None

    clicked: bool
    seen: bool
    days_left: NonNegativeInt = None

    result: NonNegativeFloat = None
