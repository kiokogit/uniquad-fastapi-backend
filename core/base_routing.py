from fastapi import APIRouter, Depends
from core.dependencies import token_bearer


main_router = APIRouter(dependencies=[Depends(token_bearer)], prefix="/api/v1")

