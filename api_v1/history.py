from fastapi import APIRouter
from components import db

router = APIRouter()

@router.get('/getAllItem')
def getAllItem():
    UserId = '1'
    q = 'select distinct OrderId, code, UserName, Phone, OrderDate, RecieveDate, Destination, status, note from history where UserId = \"'+UserId+'\" and status = \"0\" or status = \"-1\";'
    result = db.query_exec(q)
    q = 'select o.status, o.OrderId, f.*, o.quantity from history o, foods f where o.UserId = \"'+UserId+'\" and o.FoodId = f.FoodId;'
    data = db.query_exec(q)
    for r in result:
        temp1 = []
        for d in data:
            d1 = {}
            d1.update(d)
            if r['OrderId'] == d1['OrderId'] and r['status'] == d1['status']:
                d1.pop('OrderId')
                d1.pop('status')
                temp1.append(d1)
        if r['status'] == '0':
            r.update({'status':'Successed'})
        elif r['status'] == '-1':
            r.update({'status':'Cancelled'})
        r.update({'code':r['code'][2:-2]})
        r.update({'data' : temp1})
    return result

@router.get('/deleteAllItem')
def deleteAllItem():
    UserId = '1'
    q = 'Delete from history where UserId = \"1\" and status = \"0\" or status = \"-1\";'
    db.query_exec(q)
    return {'status':'oke'}