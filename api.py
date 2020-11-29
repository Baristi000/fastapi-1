from fastapi import APIRouter
from api_v1 import foods, tag, topRecent, bag, promotion, order_handler, history

api_router = APIRouter()
api_router.include_router(foods.router, prefix='/food', tags=['food'])
api_router.include_router(tag.router, prefix='/tag', tags=['tag'])
api_router.include_router(topRecent.router, prefix='/topRecent', tags=['TopRecent'])
api_router.include_router(bag.router, prefix='/bag', tags=['bag'])
api_router.include_router(promotion.router, prefix='/promotion', tags=['promotion'])
api_router.include_router(order_handler.router, prefix='/order_handler', tags=['order_handler'])
api_router.include_router(history.router, prefix='/history', tags=['history'])