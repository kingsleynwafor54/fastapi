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
    # post=find_post(id)
    cursor.execute("""select * from posts where id=%s""",(str(id),))
    post=cursor.fetchone()
    if not post:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    return {"post_detail": post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("Delete from posts where id=%s returning*",(str(id),))
    deleted_post=cursor.fetchone()
    conn.commit()
    # index=find_index_post(id)
    # if index==None:
    if deleted_post==None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Post with id:{id} does not exist")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, posts:UpdatePost):
    cursor.execute("""UPDATE posts SET title=%s, content=%s,published=%s where id=%s returning *""",(posts.title,posts.content, posts.published,id))
    updated_post=cursor.fetchone()
    conn.commit()
    if updated_post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_CONTENT,detail=f"Post with id:{id} does not exist")
    # post_dict= posts.dict()
    # index=find_index_post(id)
    # if index==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_CONTENT,detail=f"Post with id:{id} does not exist")
    # old_post=my_posts[index]
    # if index is not None:
    #     old_post=my_posts[index]
    # if post_dict["title"] is not None:
    #     old_post["title"]=post_dict["title"]
    # if post_dict["content"] is not None:
    #     old_post["content"]=post_dict["content"]  
    # if post_dict["published"] is not None:
    #     old_post["published"]=post_dict["published"]  
    # if post_dict["rating"] is not None:
    #     old_post["rating"]=post_dict["rating"]  
    return {"data":updated_post}


# from typing import Annotated

# from fastapi import Depends, FastAPI
# from fastapi.security import OAuth2PasswordBearer
# from pydantic import BaseModel

# app = FastAPI()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None


# def fake_decode_token(token):
#     return User(
#         username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
#     )


# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     return user


# @app.get("/users/me")
# async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
#     return current_user




# ----------------------------------------------------------------------------------------------
# from typing import Annotated, Literal
# from fastapi import FastAPI, Query
# from pydantic import BaseModel, Field

# from typing import Annotated, Literal
# from fastapi import FastAPI, Query
# from pydantic import BaseModel, Field
# from datetime import datetime

# app = FastAPI()

# ITEMS = [
#     {
#         "id": 1,
#         "name": "FastAPI Guide",
#         "tags": ["python", "backend",'fastAPI'],
#         "created_at": datetime(2024, 1, 10),
#         "updated_at": datetime(2024, 2, 5),
#     },
#     {
#         "id": 2,
#         "name": "Django Handbook",
#         "tags": ["python", "backend"],
#         "created_at": datetime(2024, 1, 5),
#         "updated_at": datetime(2024, 3, 1),
#     },
#     {
#         "id": 3,
#         "name": "React Basics",
#         "tags": ["frontend", "javascript"],
#         "created_at": datetime(2024, 2, 1),
#         "updated_at": datetime(2024, 2, 20),
#     },
# ]


# app = FastAPI()


# class FilterParams(BaseModel):
#     model_config = {"extra": "forbid"}  # ❌ reject unknown query params

#     limit: int = Field(100, gt=0, le=100)   # page size
#     offset: int = Field(0, ge=0)            # pagination offset
#     order_by: Literal["created_at", "updated_at"] = "created_at"
#     name: str='name'
#     tags: list[str] = []                    # filter by tags


# @app.get("/items/")
# async def read_items(
#     filters: Annotated[FilterParams, Query()]
# ):
#     results = ITEMS

#     if filters.tags:
#         results = [
#             item for item in results
#             if any(tag in item["tags"] for tag in filters.tags)
#         ]

#     results = sorted(results, key=lambda x: x[filters.name])

#     results = results[
#         filters.offset : filters.offset + filters.limit
#     ]

#     return results




# ----------------------------------------------------------------------
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user