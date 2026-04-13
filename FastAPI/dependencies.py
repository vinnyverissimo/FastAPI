from fastapi import Depends, HTTPException
from config import ALGORITHM, SECRET_KEY, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import User, Order, Itens
from jose import JWTError, jwt


def create_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


def checkToken(token: str = Depends(oauth2_schema), session: Session = Depends(create_session)):
    try:
        tokenInfo = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        userId = tokenInfo.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = session.query(User).filter(User.id == userId).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User")
    return user
