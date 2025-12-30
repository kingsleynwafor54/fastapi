from typing import Annotated, List, Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from dotenv import load_dotenv
import os
from psycopg2.extras import RealDictCursor
import time
from .import model, schemas,utils
from .model import Post
from sqlalchemy.orm import Session
from .database import engine, sessionlocal
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from .routers import post, user,auth
# Load environment variables from .env
load_dotenv()
model.Base.metadata.create_all(bind=engine)



app=FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# @app.get("/")
# async def root(db:Session=Depends(get_db)):
#     return {"message":"Hello world"}
