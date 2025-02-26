from pydantic import BaseModel
from schemas._base import NonNegativeFloat, NonNegativeInt


class Stats(BaseModel):
    impressions_count: NonNegativeInt = 0
    clicks_count: NonNegativeInt = 0
    conversion: NonNegativeInt = 0

    spent_impressions: NonNegativeFloat = 0
    spent_clicks: NonNegativeFloat = 0
    spent_total: NonNegativeFloat = 0


class DailyStats(Stats):
    date: NonNegativeInt
