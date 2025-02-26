from os import getenv
from infra import redis
from httpx import AsyncClient
from exceptions import ServiceException


MODERATION_API_URL = getenv('MODERATION_API_URL')


class ModerationService:
    async def validate_text(self, text, strict = False) -> bool:
        rate = await self.get_rate()

        if not rate > 0:
            return True

        value = await self.check_text(text)

        print(value, rate)

        if value >= rate:
            if strict:
                raise ServiceException(status_code=400, detail='Текст не соответствует установленным критериям и содержит нежелательные выражения')
            return False
        return True
            

    async def check_text(self, text: str) -> float:
        try:
            async with AsyncClient() as client:
                response = await client.post(MODERATION_API_URL, json={
                    "text": text
                })
                print(response.json())
                return float(response.json()['toxicity'])
        except Exception as e:
            print(e)
        return 0

    async def set_rate(self, value: float) -> None:
        await redis.set('moderation', value)

    async def get_rate(self) -> float:
        value = await redis.get('moderation')

        if value:
            return float(value)
        return 0
