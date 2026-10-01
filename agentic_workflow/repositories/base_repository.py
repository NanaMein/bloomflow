import os

from langchain_cohere import CohereEmbeddings
from mem0 import AsyncMemory
from redis.asyncio import Redis as AsyncRedis

from agentic_workflow.core.config import Settings

os.environ["COHERE_API_KEY"] = Settings.get_cohere_api_key()
os.environ["GROQ_API_KEY"] = Settings.get_groq_api_key()

class AsyncRedisBaseRepository:
    _redis: AsyncRedis | None = None


    @classmethod
    def redis_start(cls) -> AsyncRedis:
        if cls._redis is None:
            cls._redis = AsyncRedis.from_url("redis://127.0.0.1:6379")
        return cls._redis

    @classmethod
    async def redis_stop(cls):
        if cls._redis is not None:
            await cls._redis.aclose()
            cls._redis = None

    @classmethod
    def get_client(cls) -> AsyncRedis:
        if cls._redis is None:
            raise RuntimeError("Redis client is not initialized")
        return cls._redis



class AsyncMemZeroBaseRepository:
    _async_memory: AsyncMemory | None = None
    _memo_config: dict | None = None

    @classmethod
    def start_async_memory(cls):
        if cls._async_memory is None:
            mem_zero_config = cls.get_config()
            cls._async_memory = AsyncMemory.from_config(mem_zero_config)

    @classmethod
    def get_config(cls):
        if cls._memo_config is None:
            cls._memo_config = {
                "vector_store": {
                    "provider": "milvus",
                    "config": {
                        "url": Settings.get_milvus_uri(),
                        "token": Settings.get_milvus_token(),
                        "collection_name": Settings.get_mem_zero_collection_name(),
                        "embedding_model_dims": 1536,
                    }
                },
                "llm": {
                    "provider":"groq",
                    "config": {
                        "model": Settings.get_mem_zero_llm_model_name(),
                        "temperature": 0.3,
                        "max_tokens": 10_000,
                        "reasoning_effort": "medium",
                    }
                },
                "embedder": {
                    "provider": "langchain",
                    "config": {
                        "model": CohereEmbeddings(
                            model=Settings.get_cohere_embedding_model_name(),
                            client=None,
                            async_client=None
                        )  
                    }
                }
            }
        return cls._memo_config

    @property
    def mem_zero_client(self) -> AsyncMemory:
        if self._async_memory is None:
            raise RuntimeError("Memory client not initialized")
        return self._async_memory

    def stop_async_memory(self):
        if self._async_memory is not None:
            self._async_memory.close()
            self._async_memory = None