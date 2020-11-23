from fastapi import APIRouter
from components.db import query_exec
from components import db_handler

router = APIRouter()

@router.get('/getAllItem')
def getAllItem():
    UserId = '1'
    q = 'select * from foods, Bag where Bag.UserId = \"'+UserId+'\" and Bag.FoodId = foods.FoodId;'
    result = query_exec(q)
    result = db_handler.removeUserId(result)
    return result

@router.get('/addItem{FoodId}-{quantity}')
def addItem(FoodId,quantity):
    UserId = '1'
    if int(quantity) == 0:
        q = 'delete from Bag where UserId = \"'+UserId+'\" and FoodId = \"'+FoodId+'\"'
        query_exec(q)
    else:
        q = 'select count(*) as num from Bag where UserId = \"'+UserId+'\" and FoodId = \"'+FoodId+'\";'
        num = int(query_exec(q)[0]['num'])
        if num ==0:
            q = 'insert into Bag values(\"'+FoodId+'\",\"'+UserId+'\", '+quantity+')'
            query_exec(q)
        else:
            q = 'update Bag set quantity = '+quantity+' where UserId = \"'+UserId+'\" and FoodId = \"'+FoodId+'\";'
            query_exec(q)
    return ({'status':'oke'})