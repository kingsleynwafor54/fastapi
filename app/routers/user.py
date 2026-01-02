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
from typing import List

router=APIRouter(
    prefix="/users",tags=['Users']
)
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Annotated[Session,Depends(get_db)]):
    
    #hash th epassword- user.password
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    user=user.model_dump()
    new_user=model.User(**user)
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    db.refresh(new_user)
    return new_user


@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id:int, db:Annotated[Session, Depends(get_db)]):
    user=db.query(model.User).filter(model.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} does not exist")
    return user 


@router.get('/',response_model=List[schemas.UserOut])
def get_user( db:Annotated[Session, Depends(get_db)],limit:int=10):
    user=db.query(model.User).limit(limit).all()
    print(type(user))
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id:{id} does not exist")
    return user    