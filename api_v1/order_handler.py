from fastapi import APIRouter, HTTPException
from components import db, db_handler

router = APIRouter()

@router.get('/getAllItem')
def getAllitem():
    UserId = '1'
    q = 'select distinct OrderId, code, UserName, Phone, OrderDate, RecieveDate, Destination, note from history where UserId = \"'+UserId+'\" and status = \"1\";'
    result = db.query_exec(q)
    q = 'select o.OrderId, f.*, o.quantity from history o, foods f where o.UserId = \"'+UserId+'\" and o.FoodId = f.FoodId and o.status = \"1\";'
    data = db.query_exec(q)
    for r in result:
        temp1 = []
        r.update({'status':'Processing'})
        for d in data:
            d1 = {}
            d1.update(d)
            if r['OrderId'] == d1['OrderId']:
                d1.pop('OrderId')
                temp1.append(d1)
        r.update({'code':r['code'][2:-2]})
        r.update({'data' : temp1})
    return result

@router.get('/getOrder{OrderId}')
def getOrder(OrderId:str):
    UserId = '1'
    q = 'select distinct OrderId, code, UserName, Phone, OrderDate, RecieveDate, Destination, note from history where UserId = \"'+UserId+'\" and OrderId = \"'+OrderId+'\" and status = \"1\";'
    result = db.query_exec(q)
    q = 'select o.OrderId, f.*, o.quantity from history o, foods f where o.UserId = \"'+UserId+'\" and o.FoodId = f.FoodId and o.status = \"1\";'
    data = db.query_exec(q)
    for r in result:
        temp1 = []
        for d in data:
            d1 = {}
            d1.update(d)
            if r['OrderId'] == d1['OrderId']:
                d1.pop('OrderId')
                temp1.append(d1)
        r.update({'code':r['code'][2:-2]})
        r.update({'data' : temp1})
    return result

@router.get('/doneOrder{OrderId}')
def doneOrder(OrderId:str):
    UserId = '1'
    q = 'select count(*) as num from history where UserId = \"'+UserId+'\" and OrderId = \"'+OrderId+'\" and status = \"1\";'
    num = db.query_exec(q)[0]['num']
    if num == 0:
        raise HTTPException(status_code = 500, detail = 'Order not found')
    q = 'update history set status = \"0\" where OrderId = \"'+OrderId+'\" and UserId = \"'+UserId+'\";'
    db.query_exec(q)
    return {'status' : 'oke'}

@router.get('/cancellOrder{OrderId}')
def cancellOrder(OrderId:str, date:str, time:str):
    UserId = '1'
    q = 'select count(*) as num from history where UserId = \"'+UserId+'\" and OrderId = \"'+OrderId+'\" and status = \"1\";'
    num = db.query_exec(q)[0]['num']
    if num == 0:
        raise HTTPException(status_code = 500, detail = 'Order not found')
    q = 'update history set status = \"-1\" where OrderId = \"'+OrderId+'\" and UserId = \"'+UserId+'\";'
    db.query_exec(q)
    return {'status' : 'oke'}