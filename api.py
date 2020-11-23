from fastapi import APIRouter
from api_v1 import foods, tag, topRecent, bag

api_router = APIRouter()
api_router.include_router(foods.router, prefix='/food', tags=['food'])
api_router.include_router(tag.router, prefix='/tag', tags=['tag'])
api_router.include_router(topRecent.router, prefix='/topRecent', tags=['TopRecent'])
api_router.include_router(bag.router, prefix='/bag', tags=['bag'])