import asyncio
from uuid import UUID
from fastapi import BackgroundTasks, Request, Depends, Query, WebSocket
from sqlalchemy.orm import Session
from database.connection import get_db
from posts.models import Post, PostType
from posts.service import create_post, fetch_posts, fetch_post, act_on_post_post
from posts.schema import CreatePostSchema, DetailedPostSchema, PostSchema
from core.base_routing import main_router as router
from fastapi_pagination import Page
from search.client import client as es
from fastapi import File, UploadFile, Form
from typing import List, Optional


@router.post("/posts/create", response_model=dict)
async def create_post_route(request: Request, post: CreatePostSchema, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    response = await create_post(request, post, background_tasks, db)
    return response

@router.get("/posts/fetch", response_model=Page[PostSchema])
def fetch_posts_route(request: Request, post_type: PostType = Query(..., description="The type of post to fetch"), order_by: str = Query('newest'), db: Session = Depends(get_db)):
    return fetch_posts(request, post_type, order_by, db)

@router.get("/posts/fetch/{post_id}", response_model=DetailedPostSchema)
def fetch_post_route(request: Request, post_id: UUID, db: Session = Depends(get_db)):
    return fetch_post(request, post_id, db)

@router.post("/posts/actions/{post_id}/{action_type}")
def like_bookmark_attend(post_id: UUID, action_type: str, db:Session = Depends(get_db)):
    return act_on_post_post(post_id, action_type, db)


@router.websocket('/chat')
async def inline_chat_ws(websocket: WebSocket, post_id, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        post = db.query(Post).get(post_id)
    except:
        await websocket.close(code=1008)
        return
    while True:
        msg = websocket.receive_text()



@router.get('/posts/search')
def search_posts(query: str, category: str):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "description", "author_id"]
            }
        },
        "size": 20
    }

    response = es.search(
        body=body,
        index=category if category else 'events' 
    )
    return response


# @router.post("/posts/create_with_files", response_model=dict)
# async def create_post_with_files(
#     request: Request,
#     background_tasks: BackgroundTasks,
#     title: Optional[str] = Form(None),
#     description: str = Form(...),
#     location: Optional[str] = Form(None),
#     time: Optional[str] = Form(None),
#     attendees: Optional[int] = Form(None),
#     author_id: str = Form(...),
#     community_instance_id: Optional[str] = Form(None),
#     post_type: str = Form(...),
#     price: Optional[int] = Form(120),
#     pin_location: Optional[str] = Form(None),
#     contact: Optional[str] = Form("0703618918"),
#     parent_post_id: Optional[str] = Form(None),
#     files: Optional[List[UploadFile]] = File(None),
#     db: Session = Depends(get_db)
# ):
#     # Upload images/videos to minio and collect their UUIDs
#     image_uuids = []
#     if files:
#         for upload in files:
#             # Save uploaded file to Minio, get UUID
#             # Here, we'll make a basic compatible call to the minio client by using es._transport.client.bucket API signature for demonstration.
#             # You should replace this with your actual Minio client and proper handling.
#             file_uuid = str(uuid.uuid4())
#             content = await upload.read()
#             es._transport.client.put_object(
#                 "media-bucket",
#                 f"{file_uuid}-{upload.filename}",
#                 content,
#                 length=len(content)
#             )
#             image_uuids.append(f"{file_uuid}-{upload.filename}")

#     # Build CreatePostSchema payload
#     from datetime import datetime
#     time_val = None
#     try:
#         if time:
#             time_val = datetime.fromisoformat(time)
#     except Exception:
#         time_val = None

#     post_data = CreatePostSchema(
#         title=title,
#         description=description,
#         location=location,
#         time=time_val,
#         images=image_uuids,
#         attendees=attendees,
#         author_id=author_id,
#         community_instance_id=community_instance_id,
#         post_type=post_type,
#         price=price if price is not None else 120,
#         pin_location=pin_location,
#         contact=contact,
#         parent_post_id=parent_post_id
#     )

#     return create_post(request, post_data, background_tasks, db)


