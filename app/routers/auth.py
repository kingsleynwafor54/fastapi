from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from .. import database,schemas, model,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router=APIRouter(
    tags=['Authentication']
)

@router.post('/login')
# def login(user_credentials:schemas.UserLogin,db:Session=Depends(database.get_db)):
def login(user_credentials:OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm),db:Session=Depends(database.get_db)):
    user=db.query(model.User).filter(model.User.email==user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    if not utils.verify(user_credentials.password,user.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    #create a token
    access_token=oauth2.create_access_token(data={'users_id':user.id})
    
    return {"token":access_token,"token_type":'bearer'}