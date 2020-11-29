import random
from fastapi import APIRouter, HTTPException, Body
from components import db_handler, db

router = APIRouter()

@router.get('/getAllItem')
def getAllItem():
    UserId = '1'
    q = 'select * from promotion where UserId = \"'+UserId+'\";'
    result = db_handler.removeUserId(db.query_exec(q))
    return result

@router.get('/getItem{code}')
def getItem(code:str):
    q = 'select * from promotion where code = \"'+code+'\";'
    result = db_handler.removeUserId(db.query_exec(q))
    if len(result) == 0:
        raise HTTPException(status_code = 500, detail = 'Code not found')
    return result[0]

@router.get('/removePromotion{code}')
def removePromotion(code):
    UserId = '1'
    if len(db_handler.removeUserId(db.query_exec('select * from promotion where code = \"'+code+'\";'))) == 0:
        raise HTTPException(status_code = 500, detail = 'Code not found')
    q = 'delete from promotion where UserId = \"'+UserId+'\" and code = \"'+str(code)+'\"'
    db.query_exec(q)
    return {'status':'oke'}

@router.post('/addPromotion')
def addPromotion(
    value: str = Body(...)
):
    UserId = '1'
    code = str(random.randrange(10,99))+str(value)+str(random.randrange(10,99))
    q = 'insert into promotion values(\"'+code+'\",\"'+UserId+'\",\"'+value+'\");'
    db.query_exec(q)
    return {'code':code,
            'value':value}