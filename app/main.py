from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from dotenv import load_dotenv
import os
from psycopg2.extras import RealDictCursor
import time
# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

app=FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published:bool=True
    rating:Optional[int]=None

class UpdatePost(BaseModel):
    title: Optional[str]
    content: Optional[str]
    published:bool=True
    rating:Optional[int]=None
while True:
    try:
        conn=psycopg2.connect(host=HOST,database=DBNAME,user=USER, password=PASSWORD,cursor_factory=RealDictCursor,port=PORT)
        cursor=conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep()

my_posts=[{
        "id":1,
        "title": "Check Out this beautiful place",
        "content": "content of post 1",
        "published":True,
        "rating": None
    },{
        "id":2,
        "title": "Check Out this beautiful place",
        "content": "content of post 2",
        "published":True,
        "rating": None
    }]
def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
def find_index_post(id):
    for ix, post in enumerate(my_posts):
        if post['id']==id:
            return ix
@app.get("/")
async def root():
    return {"message":"Hello world"}

@app.get('/posts')
def get_post():
    cursor.execute(""" Select * from posts""")
    posts=cursor.fetchall()
    return {"data": posts}

@app.post('/posts',status_code=status.HTTP_201_CREATED)
# def create_post(post: dict=Body(...)):
def create_post(posts:Post):
    # post_dict= posts.dict() 
    # post_dict['id']==randrange(0,1000)
    # # post_dict['id']=len(my_posts)+1
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s,%s,%s) RETURNING *""",(posts.title,posts.content, posts.published))
    new_post=cursor.fetchone()
    conn.commit()
    
    return {"data":new_post}
    # return {"post_dict": f"title:{post['title']} content:{post['content']}"}

@app.get('/posts/{id}')
def get_post(id:int,response:Response):
    post=find_post(id)
    if not post:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    return {"post_detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_CONTENT,detail=f"Post with id:{id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, posts:UpdatePost):
    post_dict= posts.dict()
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_CONTENT,detail=f"Post with id:{id} does not exist")
    old_post=my_posts[index]
    if index is not None:
        old_post=my_posts[index]
    if post_dict["title"] is not None:
        old_post["title"]=post_dict["title"]
    if post_dict["content"] is not None:
        old_post["content"]=post_dict["content"]  
    if post_dict["published"] is not None:
        old_post["published"]=post_dict["published"]  
    if post_dict["rating"] is not None:
        old_post["rating"]=post_dict["rating"]  
    return {"data":old_post}
