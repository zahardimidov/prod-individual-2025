from infra import redis
from infra.config import settings
from infra.repository import CurrentDateRepository


class TimeAdvanceService:
    def __init__(self):
        self.repo = CurrentDateRepository()

    async def set_date(self, value) -> int:
        current_date = await self.get_instance()
        
        await self.repo.update(id=current_date.id, value=value)

        if not settings.TEST_MODE:
            await redis.set('current_date', value)

        return value

    async def get_date(self) -> int:
        if not settings.TEST_MODE:
            value = await redis.get('current_date')

            if value is not None:
                return int(value)

        current_date = await self.get_instance()

        if not settings.TEST_MODE:
            await redis.set('current_date', current_date.value)

        return current_date.value

    async def get_instance(self):
        current_date = await self.repo.get_all()
        if current_date:
            return current_date[0]
        return await self.repo.create(value=0)
