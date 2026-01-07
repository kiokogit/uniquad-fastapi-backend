from celery import Celery, shared_task
from fastapi import Depends
from database.connection import get_db
from sqlalchemy.orm import Session
from core.settings import settings
from search.client import client as es

celery_app = Celery(
    'worker',
    broker=settings.BROKER_URL,
    backend="rpc://"
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='Africa/Nairobi',
    enable_utc=True,
    result_expires=90000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_ignore_result=False,
    task_store_eager_result=True,
    # beat_scheduler="app.celery_beat:",
)


@celery_app.task(bind=True)
def index_documents(self, index: str, documents: list[dict]):
    # create_index_if_does_not_exist(index)
    
    for rec in documents:
        es.index(index=index, document=rec)
    
