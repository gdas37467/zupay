from fastapi import FastAPI, Depends, HTTPException, status,Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Annotated
from database import usersCollection
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


async def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = authorization.credentials
        
        
       # print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
       # print(payload)
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        
    except JWTError as e:
        print(e)
        raise credentials_exception
    user = await usersCollection.find_one({'email' : email})
    if user is None:
        raise credentials_exception
    print(user)
    return user