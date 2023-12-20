from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, HTTPException
from sqlalchemy.orm import Session
from sql_app.db.repository import crud
from sql_app.db.session import get_db
 
from sql_app.schemas import schemas
from sql_app.core.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
 

router = APIRouter(tags=["Authentication"] )

 

@router.post("/login", )
def login(user: schemas.UserCreate ,db:Session = Depends(get_db)):
    try:
        db_user = crud.login(db , email=user.email,password=user.password )
        if not db_user:
            raise HTTPException(status_code=401, detail="Incorrect username or password") 
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"userId": db_user.id,"scope": "access_token"}, expires_delta=access_token_expires)
        raise HTTPException(status_code=200, detail={"token": access_token})
    except HTTPException as ex: 
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
       

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if not user.email:
            raise HTTPException(status_code=400, detail="Email cannot be empty")
        else:
            db_user = crud.get_user_by_email(db, email=user.email)
            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            return crud.create_user(db=db, user=user)
    except HTTPException as ex:
        print(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)