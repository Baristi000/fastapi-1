import os, random
from base64 import b64decode
from typing import List, Optional
from fastapi import APIRouter, Body, HTTPException
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
    name = FoodType+str(random.randrange(1,1001))+'.png'                        #create new name
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
            print("Remove image "+str(ImagePath)+" successfull!")
        except OSError as error:
            print(error)
    return ({'status':'oke'})

@router.post('/editFood')
async def editFood(
    FoodId: str = Body(...),
    ImageUrl: str = Body(...),
    FoodType: str = Body(...),
    Rating: str = Body(...),
    Price: str = Body(...),
    Title: str = Body(...),
    Content: str = Body(...)
    ):
    file = str(ImageUrl)
    #check whether FoodId existed or not
    q = 'select count(*) as num from foods where FoodId = \"'+FoodId+'\";'
    num = query_exec(q)[0]['num']
    if num == 0:
        raise HTTPException(status_code = 500, detail = 'FoodId not found')
    else:
        #update image in folder './api_v1/img' if change
        if '/png;base64,' in str(file):
            #delete image
            q = 'select ImageUrl from foods where FoodId = \"'+FoodId+'\";'             #create get image url query
            ImageUrl = str(query_exec(q)).split("/")                                    #get image url
            ImagePath = str(ImageUrl[len(ImageUrl)-1].strip("\'}]"))
            try:                                                                        #delete image
                os.remove('./api_v1/img/'+ImagePath)                                        
                print("Remove image "+str(ImagePath)+" successfull!")
            except OSError as error:
                print(error)
            #store new image
            ih.mk_dir('./api_v1/img')                                                   #create dir
            file = file.split(',')[1]
            file = b64decode(file, validate = True)
            img = ih.Iconverse(file)                                                    #read image
            name = FoodType+str(random.randrange(1,1001))+'.png'                        #create new name
            img.save("./api_v1/img/"+str(name))                                         #save image with new name
            ImageUrl = 'http://'+str(settings.IMG_HOST)+':'+str(settings.PORT)+'/getImage/'+str(name) #creaet image url
        else:
            ImageUrl = file
        #update data in database at table foods
        q = 'update foods set FoodType = \"'+FoodType+'\", Rating = \"'+FoodType+'\", Price = \"'+Price+'\", Title = \"'+Title+'\", Content = \"'+Content+'\", ImageUrl = \"'+ImageUrl+'\" where FoodId = \"'+FoodId+'\";'
        query_exec(q)
    return {'status' : 'oke'}