from typing import Optional,Union
from bson.objectid import ObjectId

from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    tags: list = Field(...)
 

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "password": "xxxxxxxxxx",
                "tags": ['Science','english'],
              
            }
        }

class UpdateProfile(BaseModel):
    fullname: Optional[str]  = None
    email: Optional[EmailStr]  = None 
    password: Optional[str] =None
 

    class Config:
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
                "password": "xxxxxxxxxx",
                "tags": ['Science','english'],
              
            }
        }


class SignInSchema(BaseModel):

    email: EmailStr = Field(...)
    password: str = Field(...)

 

    class Config:
        schema_extra = {
            "example": {
            
                "email": "jdoe@x.edu.ng",
                "password": "xxxxxxxxxx",
        
              
            }
        }


class BlogSchema(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    tags: list = Field(...)

class UpdateBlog(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[list] = None
   
    
def ResponseModel(data, message):
    return ({
        "data": data,
        "code": 200,
        "message": message,
    })


def ErrorResponseModel(error, code, message):
    return JSONResponse(status_code=code ,content={"error": error, "code": code, "message": message})