
from pydantic import BaseSettings
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class Settings(BaseSettings):
  #dbconfig  
    MYSQL_SERVER = "localhost"
    MYSQL_USER = "mobile_db"
    MYSQL_PASSWORD = "tdt2020"
    MYSQL_DB = "mobile_db1"
  #server config

   # Trieu's macbook pro hamachi host ip
    HOST = '25.71.124.112'
    IMG_HOST = '25.71.124.112'
    PORT = 8000
    

    #image host raspberry
    IMG_HOST = 'tdtsv.ddns.net'
    HOST = '192.168.1.12'
    PORT = 8000
  #var


settings = Settings()