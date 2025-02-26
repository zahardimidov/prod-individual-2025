from schemas._base import RequestModel, NonEmptyStr, NonNegativeFloat
from pydantic import BaseModel, Field


class GenerateText(RequestModel):
    advertiser_name: NonEmptyStr = Field(description='Название рекламодателя')
    ad_title: NonEmptyStr = Field(description='Название рекламы')


class GenerateTextResponse(BaseModel):
    text: NonEmptyStr = Field(description='Результат генерации рекламного текста')


class Text(RequestModel):
    text: NonEmptyStr = Field(description='Текст для модерации')

class TextCheckResponse(RequestModel):
    toxicity: NonNegativeFloat = Field(description='Степень неблагоприятности текста')


class ModerationRate(RequestModel):
    rate: NonNegativeFloat = Field(description='Строгость модерации текста (минимальная степень неблагоприятности для бана)')


class TextModerationResponse(BaseModel):
    is_valid: bool