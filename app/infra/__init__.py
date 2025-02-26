from infra.config import settings
from redis.asyncio import from_url


class redis:
    url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'

    @staticmethod
    async def flush():
        async with from_url(redis.url) as async_redis:
            print('fluuuushhh')
            await async_redis.flushdb()

    @staticmethod
    async def set(key, value, ex=None):
        async with from_url(redis.url) as async_redis:
            return await async_redis.set(str(key), value, ex=ex)

    @staticmethod
    async def get(key) -> bytes:
        async with from_url(redis.url) as async_redis:
            return await async_redis.get(str(key))

    @staticmethod
    async def delete(key):
        async with from_url(redis.url) as async_redis:
            return await async_redis.delete(str(key))
