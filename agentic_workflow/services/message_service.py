import json

from redis.exceptions import RedisError

from ..repositories.base_repository import AsyncRedisBaseRepository


class MessageServiceError(Exception):
    def __init__(self, message: str, status_code: int):
        self.status_code = status_code
        super().__init__(message)


class MessageService:
    def __init__(self, with_limit: bool = False, max_limit: int = 15):
        self._redis_client = AsyncRedisBaseRepository.get_client()
        self._with_limit = with_limit
        self._max_limit = max_limit

    def limit_messages(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        if self._with_limit:
            return messages[-self._max_limit:]
        return messages

    def convert_bytes_to_list(self, input: bytes) -> list[dict[str, str]]:
        data_list = json.loads(input)
        if not data_list:
            return []
        return data_list

    def convert_list_to_bytes(self, input: list) -> bytes:
        data_str = json.dumps(input)
        return data_str.encode('utf-8')
        

    async def redis_set(self, *args) -> bool:
        try:
            result = await self._redis_client.set(*args)
        except RedisError as e:
            raise MessageServiceError(f"Redis set failed: {e!s}", status_code=500)

        if result is not True:
            raise MessageServiceError(f"Redis set failed: expected True, got {result!s}", status_code=400)

        return True

    async def redis_get(self, *args):
        try:
            return await self._redis_client.get(*args)
        except RedisError as e:
            raise MessageServiceError(f"Redis get failed: {e!s}", status_code=500)


    async def get_raw_messages(self, user_id: str) -> bytes:
        current_messages = await self.redis_get(user_id)
        if isinstance(current_messages, bytes):
            return current_messages
        raise MessageServiceError("Redis returned non-bytes value. Please re-check Redis configuration", status_code=400)


    async def get_messages(self, user_id: str) -> list[dict[str, str]]:
        raw_byte_messages = await self.get_raw_messages(user_id)
        return self.convert_bytes_to_list(raw_byte_messages)

    async def add_user_message(self, user_id: str, message: str) -> bool:
        current_messages = await self.get_messages(user_id)
        new_user_message = {"role": "user", "content": message}
        current_messages.append(new_user_message)
        current_messages = self.limit_messages(current_messages)
        return await self.redis_set(user_id, self.convert_list_to_bytes(current_messages))

    async def add_ai_message(self, user_id: str, message: str) -> bool:
        current_messages = await self.get_messages(user_id)
        new_ai_message = {"role": "assistant", "content": message}
        current_messages.append(new_ai_message)
        current_messages = self.limit_messages(current_messages)
        return await self.redis_set(user_id, self.convert_list_to_bytes(current_messages))