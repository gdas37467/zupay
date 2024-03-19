from fastapi import APIRouter,Depends
from models import UserSchema,ResponseModel,ErrorResponseModel,SignInSchema,UpdateProfile
from fastapi import Body
from fastapi.encoders import jsonable_encoder
from database import usersCollection
from jose import jwt, JWTError
from typing import Annotated
from middleware import get_current_user
router = APIRouter()
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

@router.post('/register',response_description='New User Registered')
async def registerUser(user: UserSchema= Body(...)):
    user = jsonable_encoder(user)
    findUser = await usersCollection.find_one(user)
    if findUser : 
        return ErrorResponseModel('DuplicateUser',500,'User Already Exists')
    newUser = await usersCollection.insert_one(user)
    user_data = {"email": user['email']}
    jwt_token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
   
    return ResponseModel({"token": jwt_token}, "User added successfully.")

@router.post('/signin',response_description='Token Generated')
async def registerUser(user: SignInSchema= Body(...)):
    user = jsonable_encoder(user)
    findUser = await usersCollection.find_one(user)
    if not findUser : 
        return ErrorResponseModel('Invalid User',403,'User Doesnot Exists')
    user_data = {"email": user['email']}
    jwt_token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return ResponseModel({"token": jwt_token}, "Signed In successfully.")

@router.post('/signin',response_description='Token Generated')
async def registerUser(user: SignInSchema= Body(...)):
    user = jsonable_encoder(user)
    findUser = await usersCollection.find_one(user)
    if not findUser : 
        return ErrorResponseModel('Invalid User',403,'User Doesnot Exists')
    user_data = {"email": user['email']}
    jwt_token = jwt.encode(user_data, SECRET_KEY, algorithm=ALGORITHM)
    
    return ResponseModel({"token": jwt_token}, "User added successfully.")

@router.patch('/update-profile',response_description='User Details updated')
async def registerUser( newUserData:UpdateProfile= Body(...), user: dict =   Depends(get_current_user)):
    print(newUserData)
    newUserData = jsonable_encoder(newUserData)
    updateData = {}
    for key , value in newUserData.items():
        if newUserData[key] != None : 
            updateData[key] = value
    try:
    
        newvalues = {"$set" : updateData}
        await usersCollection.update_one(user,newvalues)
    except Exception as e:
        print(e)
        return ErrorResponseModel("Internal serve error",500,"Something went wrong while fetching the blog") 
    return ResponseModel({}, "User details updated successfully.")

@router.patch('/update-tag/',response_description='User Tags updated')
async def updateTagToUser(action : str , tag : str, user : dict = Depends(get_current_user)):
    try:
        if action == "add" : 
            tags = user["tags"]
           #
            tags.append(tag)
           # print(user["tag"])
            await usersCollection.update_one({"_id" : user["_id"]},{"$set": {"tags" : tags} })
            return ResponseModel({},"Tag Updated")
        elif action == "remove" : 
            tags = user["tags"]
            tags.remove(tag)
            await usersCollection.update_one({"_id" : user["_id"]},{"$set": {"tags" : tags }})
            return ResponseModel({},"Tag Updated")
        else:
            return ErrorResponseModel("Internal Server Error",500,"Invalid Action")
    except Exception as e:
        print(e)
        return ErrorResponseModel("Internal Server Error",500,"Something Went Wrong")