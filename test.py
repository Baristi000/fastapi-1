from fastapi import FastAPI, File, UploadFile, Body
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import uvicorn, random
from components.db import query_exec
from components import img_handler
from core.config import settings
from api import api_router
#declare app
app = FastAPI()
#allow access on all routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#get image manualy
@app.get("/getImage/{path}",tags = ['image'])
def get_image(path):
    dir = './api_v1/img/'+str(path)
    return(FileResponse(dir))
#run api command using uvicorn
if __name__ == '__main__':
    uvicorn.run('test:app', host = settings.HOST, port = settings.PORT, reload = True)
    
#run routers
app.include_router(api_router)