from datetime import timedelta

from redis.exceptions import RedisError

from .base_repository import AsyncRedisBaseRepository


class MessageRepository:
    default_expiration = timedelta(days=5)
    
    def __init__(self):
        self.r = AsyncRedisBaseRepository.get_client()

    async def set_key(
        self,
        key: str | bytes,
        value: str | bytes,
        expiration: timedelta | None = None,
        **kwargs,
    ) -> bool:
        try:
            await self.r.set(
                name=key,
                value=value,
                ex=expiration or self.default_expiration,
                **kwargs,
            )
            return True
        except RedisError as re:
            print(re)
            return False

    async def get_value(
        self,
        key: str | bytes,
    ) -> bytes | str:
        try:
            value = await self.r.get(key)
            if isinstance(value, bytes):
                return value
            raise ValueError("Value is not bytes")
        except (RedisError, ValueError) as re:
            return str(re)


    async def set_key_and_value(
        self,
        key: str | bytes,
        value: str | bytes,
        expiration: timedelta | None = None,
        **kwargs,
    ) -> bool:
        try:
            await self.r.set(
                name=key,
                value=value,
                ex=expiration or self.default_expiration,
                **kwargs,
            )
            return True
        except RedisError as re:
            print(re)
            return False

    async def get_value_by_key(
        self,
        key: str | bytes,
    ) -> bytes:
        value = await self.r.get(key)
        if isinstance(value, bytes):
            return value
        raise ValueError("Value is not bytes. Redis should return bytes because decode_responses is False")