import random
from fastapi import APIRouter, Body
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

@router.post('/purchase')
def purchase(
    data : list = Body(...),
    code : str = Body(...),
    UserName : str = Body(...),
    Phone : str = Body(...),
    OrderDate : str = Body(...),
    RecieveDate : str = Body(...),
    Destination : str = Body(...),
    note : str = Body(...)
    ):
    UserId = '1'
    OrderId = str(random.randrange(0,999))+str(data[0]['FoodId'])+str(UserId)+str(code)
    for item in data:                           #add new order into order_handler table 
        FoodId = item['FoodId']
        quantity = item['quantity']
        code = str(code)
        q = 'insert into history values (\"'+str(UserId)+'\",\"'+str(OrderId)+'\",\"'+str(FoodId)+'\",\"'+str(quantity)+'\",\"'+UserName+'\",\"'+Phone+'\",\"'+str(code)+'\",\"1\",\"'+OrderDate+'\",\"'+RecieveDate+'\",\"'+Destination+'\",\"'+note+'\");'
        query_exec(q)
    for item in data:                           #delete items in bag after purchase
        q = 'delete from Bag where UserId = \"'+UserId+'\" and FoodId = \"'+item['FoodId']+'\";'
        query_exec(q)
    if code != '':                              #delete code after use
        q = 'delete from promotion where UserId = \"'+UserId+'\" and code = \"'+code+'\"'
        query_exec(q)
    return {'status':'oke'}
