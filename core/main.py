from fastapi import FastAPI
from core.api import include_routers
from database.connection import Base, engine
from acl.models import *
from posts.models import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI(
    title="UniQuad",
    description="UniQuad is a platform for closed ecosystem engagements like universities and their environments.",
    version="0.0.1"
) 
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

add_pagination(app)

# register routes
include_routers(app)

# create database tables
Base.metadata.create_all(bind=engine)
