import os
from PIL import Image
from io import BytesIO

def mk_dir(path:str):
    try:
        os.mkdir(path)
        print("Successfull create directory "+path)
    except OSError as error:
        print(error)

def Iconverse(raw_data:bytes):
    stream = BytesIO(raw_data)
    img = Image.open(stream).convert("RGBA")
    stream.close()
    return img