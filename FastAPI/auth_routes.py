from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import checkToken, create_session
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, bcrypt_context
from schemas import UserSchema, loginSchema
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def createToken(user: User):
    expDate = datetime.now(timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dicInfo = {"sub": str(user.id), "username": user.username, "exp": expDate}
    token = jwt.encode(dicInfo, SECRET_KEY, algorithm=ALGORITHM)
    return token


@auth_router.get("/")
async def read_root():
    return {"message": "Welcome to the authentication API"}


@auth_router.post("/login")
async def login(loginSchema: loginSchema, session=Depends(create_session)):
    user = session.query(User).filter(User.email == loginSchema.email).first()
    if not user or not bcrypt_context.verify(loginSchema.hashed_password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    else:
        access_token = createToken(user)
        return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/login-form")
async def loginForm(formData: OAuth2PasswordRequestForm = Depends(), session=Depends(create_session)):
    user = session.query(User).filter(User.email == formData.username).first()
    if not user or not bcrypt_context.verify(formData.password, user.hashed_password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    else:
        access_token = createToken(user)
        return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register")
async def register(userSchema: UserSchema, session=Depends(create_session), user: User = Depends(checkToken)):

    # if not user.admin:
    #    raise HTTPException(
    #        status_code=403, detail="Only admin users can register new users")

    user = session.query(User).filter((User.email == userSchema.email)
                                      | (User.username == userSchema.username)).first()
    if user:
        raise HTTPException(
            status_code=400, detail="Email or username already registered")
    else:
        hashed_password = bcrypt_context.hash(userSchema.hashed_password)

        new_user = User(username=userSchema.username, email=userSchema.email,
                        hashed_password=hashed_password, active=userSchema.active, admin=userSchema.admin)
        session.add(new_user)
        session.commit()
        return {"message": f"User registered successfully with email: {userSchema.email} and username: {userSchema.username}"}


@auth_router.get("/refresh")
async def refresh_token(user: User = Depends(checkToken)):
    access_token = createToken(user)
    return {"access_token": access_token, "token_type": "bearer"}
