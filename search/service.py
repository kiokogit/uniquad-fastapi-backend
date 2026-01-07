from typing import Union
from fastapi import APIRouter
from .client import client as es

router = APIRouter(prefix='analytics/')

@router.get('/search')
def search_posts(query: str, category: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "author_id"]
            },
        },
        "size": 20
    }

    response = es.search(
        body=body,
        index=category if category else 'events' 
    )
    return response

