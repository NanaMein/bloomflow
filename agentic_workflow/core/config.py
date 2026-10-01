import os

from dotenv import load_dotenv

load_dotenv()



class Settings:

    @staticmethod
    def get_groq_api_key():
        return os.getenv("GROQ_API_KEY", None)

    @staticmethod
    def get_cohere_api_key():
        return os.getenv("COHERE_API_KEY", None)

    @staticmethod
    def get_milvus_uri():
        return os.getenv("MILVUS_URI", None)

    @staticmethod
    def get_milvus_token():
        return os.getenv("MILVUS_TOKEN", None)

    @staticmethod
    def get_mem_zero_collection_name():
        return os.getenv("MEM_ZERO_COLLECTION_NAME", "mem_zero_collection")

    @staticmethod
    def get_cohere_embedding_model_name():
        return os.getenv("COHERE_EMBEDDING_MODEL_NAME", "embed-v4.0")

    @staticmethod
    def get_mem_zero_llm_model_name():
        return os.getenv("MEM_ZERO_LLM_MODEL_NAME", "openai/gpt-oss-120b")