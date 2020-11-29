from typing import List, Optional
from fastapi import APIRouter, Header
from components.db import query_exec
from components import db_handler

router = APIRouter()

def invertData(Data):
    newData = []
    i = len(Data)-1
    while(i>=0):
        newData.append(Data[i])
        i-=1
    return newData

@router.get('/getAllItem')
def getAllItem():
    UserId = '1'
    q = 'select * from foods, TopRecent where TopRecent.UserId = \"'+UserId+'\" and foods.FoodId = TopRecent.FoodId ;'
    maindata = invertData(query_exec(q))
    maindata = db_handler.removeUserId(maindata)
    q = 'select * from Bag where UserId = \"'+UserId+'\";'
    tempdata = db_handler.removeUserId(query_exec(q))
    result = db_handler.joindata(maindata, tempdata, 'FoodId', 'quantity', 0)
    return result

@router.get('/updateTopRecent{FoodId}')
def updateTopRecent(FoodId):
    UserId = '1'
    int(FoodId)
    limitTopRecent = 5
    q = 'delete from TopRecent where FoodId = \"'+FoodId+'\";'
    query_exec(q)
    q = "select count(*) as cur_num from TopRecent;"
    result = query_exec(q)
    cur_num = int(result[0]['cur_num'])
    if cur_num >= limitTopRecent :
        q = 'select * from TopRecent;'
        last_id = query_exec(q)[0]['FoodId']
        q = 'delete from TopRecent where FoodId = \"'+last_id+'\";'
        query_exec(q)
    q = 'insert into TopRecent values(\"'+FoodId+'\", \"1\")'
    result = query_exec(q)
    q = 'select * from foods, TopRecent where TopRecent.UserId = \"'+UserId+'\" and foods.FoodId = TopRecent.FoodId ;'
    maindata = invertData(query_exec(q))
    maindata = db_handler.removeUserId(maindata)
    q = 'select * from Bag where UserId = \"'+UserId+'\";'
    tempdata = db_handler.removeUserId(query_exec(q))
    result = db_handler.joindata(maindata, tempdata, 'FoodId', 'quantity', 0)
    return result