from fastapi import APIRouter, Depends
from core.dependencies import TokenBearer


main_router = APIRouter(dependencies=[Depends(TokenBearer())], prefix="/api/v1")

