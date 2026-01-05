from acl.routers import router as auth_router
from posts.routers import router as posts_router
from fastapi import FastAPI


def include_routers(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(posts_router)

