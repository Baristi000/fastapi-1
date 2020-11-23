import os, random
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form
from components.db import query_exec
from components import img_handler
from core.config import settings

router = APIRouter()
ih = img_handler

@router.get('/getAllFood')
def getAllFoods():
    q = 'select * from foods'
    result = query_exec(q)
    return result

@router.get('/getFood{FoodType}')
def getSomeFoods(FoodType):
    q = 'select * from foods where FoodType = \"'+FoodType+'\"'
    result = query_exec(q)
    return result

@router.post('/addNewFood')
async def addNewFood(
    file: UploadFile = File(...),
    FoodType: str = Form(...),
    Rating: str = Form(...),
    Price: str = Form(...),
    Title: str = Form(...),
    Content: str = Form(...)
    ):
    #handel image
    ih.mk_dir('./api_v1/img')                                                   #create dir
    img = ih.Iconverse(await file.read())                                       #read image
    name = FoodType+Title+str(random.randrange(1,1001))+'.png'                  #create new name
    img.save("./api_v1/img/"+str(name))                                         #save image with new name
    ImageUrl = 'http://'+str(settings.IMG_HOST)+':'+str(settings.PORT)+'/getImage/'+str(name) #creaet image url
    q = 'insert into foods(FoodType, Rating, Price, Title, Content, ImageUrl) values(\"'+FoodType+'\",\"'+Rating+'\",\"'+Price+'\",\"'+Title+'\",\"'+Content+'\",\"'+ImageUrl+'\");'
    query_exec(q)                                                               #store data into database
    return({'status':'oke'})

@router.get('/deleteFood{FoodId}')
async def deleteFood(FoodId):
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
