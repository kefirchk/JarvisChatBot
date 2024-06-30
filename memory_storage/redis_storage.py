from settings import settings
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis


redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
storage = RedisStorage(redis=redis)
