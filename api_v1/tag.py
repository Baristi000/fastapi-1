from typing import List, Optional
from fastapi import APIRouter, Header, Body
from components.db import query_exec

router = APIRouter()

@router.get('/getAllTags')
def getAllTags():
    q = 'select * from tags;'
    result = query_exec(q)
    return result

@router.get('/getSomeTag-TagId')
async def getSomeTag_TagId(TagId: Optional[List[str]] =  Header(None)):
    q = 'select * from tags where '
    result = []
    for item in TagId:
        result.append(await query_exec(q+' TagId = '+str(item)+';'))
    result = query_exec(q)
    return result

@router.get('/getSomeTag-FoodId')
async def getSomeTag_FoodId(TagId: Optional[List[str]] =  Header(None)):
    q = 'select * from tags where '
    result = []
    for item in TagId:
        result.append(await query_exec(q+' FoodId = '+str(item)+';'))
    result = query_exec(q)
    return result

@router.post('/updateTags')
def updateTags(FoodId: str = Body(...), TagContent: str = Body(...)):
    q = 'update table tags set TagContent = \"'+TagContent+'\" where FoodId = \"'+FoodId+'\";'
    query_exec(q)
    return ({'status':'oke'})