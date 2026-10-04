from fastapi import APIRouter, HTTPException, Depends
from app.models.user_models import User, UserLoginModel, UserCreateModel
from sqlalchemy.orm import Session 
from app.db.db import getDb
from app.services.auth_service import hashPassword, verifyPassword, createAccessToken

auth_route = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_route.post("/signup")
def create_user(user:UserCreateModel,db:Session = Depends(getDb)):
    newUser = User(
        name = user.name,
        username = user.username,
        password = hashPassword(user.password),
        role= user.role,
        email = user.email
    )
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return{
        "message":"User created successfully",
        "user": newUser.id
    }

@auth_route.post("/login")
def user_login(user:UserLoginModel, db:Session= Depends(getDb)):
    findUser = db.query(User).filter(User.email == user.email).first()
    if not findUser:
        raise HTTPException(
            status_code=404,
            detail='This email not exist'
        )
    if verifyPassword(user.password, findUser.password):
        token = createAccessToken({
            "sub":str(findUser.id),
            "username":findUser.username,
            "role":findUser.role,
            "email":findUser.email
        })
        return{
            "message":"User login successfully",
            "user":{
                "id":findUser.id,
                "name":findUser.name,
                "email":findUser.email
            },
            "auth_token":token
        }
    raise HTTPException(
        status_code=400,
        detail="Wrong credentials"
    )