from .. import model, schemas, utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from typing import Annotated, List, Optional
from ..model import Post
from sqlalchemy.orm import Session
from ..database import engine, sessionlocal,get_db
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from ..import oauth2

router=APIRouter(
     prefix="/posts",tags=["Posts"]
)


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.Post, db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    new_post=model.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return {'data':new_post}

@router.get('/')
def get_post(db:Annotated[Session,Depends(get_db)],  
             response_model=List[schemas.PostResponse],
             skip: int = 0,
             limit: int = 10,current_user:int=Depends(oauth2.get_current_user)):
        total = db.query(model.Post).count()

        posts = (
            db.query(model.Post)
            .offset(skip)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": posts
        }


@router.get('/{id}')
def get_posts(id:int,db: Annotated[Session, Depends(get_db)],response:Response,current_user:int=Depends(oauth2.get_current_user)):
    posts = db.query(model.Post).filter(model.Post.id==id).first()
    if not posts:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    return {"post_detail": posts}

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Annotated[Session,Depends(get_db)]):
    query_post=db.query(model.Post).filter(model.Post.id==id)
    if query_post==None:
        # response.status_code=404
        # response.status_code=status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')

    query_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}')
def update_post(id:int, posts:schemas.PostBase,db:Annotated[Session,Depends(get_db)],
                 response_model=schemas.PostResponse,current_user:int=Depends(oauth2.get_current_user)):
    post_query=db.query(model.Post).filter(model.Post.id==id)
    post=post_query.first()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id:{id} was not found')
    
    post_query.update(posts.model_dump(exclude_unset=True),synchronize_session=False)
    db.commit()
    db.refresh(post)

    return post
