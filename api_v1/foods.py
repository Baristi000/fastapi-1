import os, random
from base64 import b64decode
from typing import List, Optional
from fastapi import APIRouter,Body
from components.db import query_exec
from components import img_handler, db_handler
from core.config import settings

router = APIRouter()
ih = img_handler

@router.get('/getAllFood')
def getAllFoods():
    UserId = '1'
    q = 'select * from foods;'
    maindata = query_exec(q)
    q = 'select * from Bag where UserId = \"'+UserId+'\";'
    tempdata = db_handler.removeUserId(query_exec(q))
    result = db_handler.joindata(maindata, tempdata, 'FoodId', 'quantity', 0)
    return result

@router.get('/getFood{FoodType}')
def getSomeFoods(FoodType):
    UserId = '1'
    q = 'select * from foods where FoodType = \"'+FoodType+'\";'
    maindata = query_exec(q)
    q = 'select * from Bag where UserId = \"'+UserId+'\";'
    tempdata = db_handler.removeUserId(query_exec(q))
    result = db_handler.joindata(maindata, tempdata, 'FoodId', 'quantity', 0)
    return result

@router.post('/addNewFood')
async def addNewFood(
    file: str = Body(...),
    FoodType: str = Body(...),
    Rating: str = Body(...),
    Price: str = Body(...),
    Title: str = Body(...),
    TagContent: str = Body(...),
    Content: str = Body(...)
    ):
    #handel image
    ih.mk_dir('./api_v1/img')                                                   #create dir
    file = file.split(',')[1]
    file = b64decode(file, validate = True)
    img = ih.Iconverse(file)                                                    #read image
    name = FoodType+Title+str(random.randrange(1,1001))+'.png'                  #create new name
    img.save("./api_v1/img/"+str(name))                                         #save image with new name
    ImageUrl = 'http://'+str(settings.IMG_HOST)+':'+str(settings.PORT)+'/getImage/'+str(name) #creaet image url
    q = 'insert into foods(FoodType, Rating, Price, Title, Content, ImageUrl) values(\"'+FoodType+'\",\"'+Rating+'\",\"'+Price+'\",\"'+Title+'\",\"'+Content+'\",\"'+ImageUrl+'\");'
    query_exec(q)                                                               #store data into database(foods table)
    # Tags handling    
    q = 'select FoodId from foods where ImageUrl = \"'+ImageUrl+'\";'
    FoodId = query_exec(q)[0]['FoodId']
    q = 'insert into tags values (\"'+str(FoodId)+'\",\"'+str(TagContent)+'\")'
    query_exec(q)
    return({'status':'oke'})

@router.post('/deleteFood')
async def deleteFood(FoodIds : list = Body(...)):
    for FoodId in FoodIds:
        q = 'select ImageUrl from foods where FoodId = \"'+FoodId+'\";'             #create get image url query
        ImageUrl = str(query_exec(q)).split("/")                                    #get image url
        ImagePath = str(ImageUrl[len(ImageUrl)-1].strip("\'}]"))                    #get image name
        q = 'delete from foods where FoodId = \"'+FoodId+'\";'                      #create delete query
        query_exec(q)                                                               #delete data in table foods
        q = 'delete from TopRecent where FoodId = \"'+FoodId+'\";'                  
        query_exec(q)                                                               #delete data in table TopRecent
        try:                                                                        #delete image
            os.remove('./api_v1/img/'+ImagePath)                                        
            print("Remove successfull!")
        except OSError as error:
            print(error)
    return ({'status':'oke'})
