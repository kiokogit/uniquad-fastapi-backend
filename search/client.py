from elasticsearch import Elasticsearch
from core.settings import settings

client = Elasticsearch(
    settings.ELASTICSEARCH_URL,
    api_key=settings.ELASTICSEARCH_API_KEY
)


