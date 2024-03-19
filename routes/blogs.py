from fastapi import APIRouter,Depends
from models import UserSchema,ResponseModel,ErrorResponseModel,SignInSchema,UpdateProfile,BlogSchema,UpdateBlog
from fastapi import Body
from fastapi.encoders import jsonable_encoder
from database import usersCollection
from database import blogCollection
from jose import jwt, JWTError
from typing import Annotated
from middleware import get_current_user
from bson import ObjectId
router = APIRouter()


@router.post('/create',response_description='Blog Created')
async def createBlog( blogData : BlogSchema = Body(...), user: dict =  Depends(get_current_user)):
    blogData = jsonable_encoder(blogData)

    try:
        blogData["author"] = user['_id']
        await blogCollection.insert_one(blogData)
    except Exception as e:
        print(e)
        return ErrorResponseModel("Something went wrong while creating the blog",500,"Blog not created")


    
    return ResponseModel({}, "Blog Created Successfully.")

@router.get('/{page}',response_description="Blogs Fetched sorted") 
async def getBlogs(page : int ,user: dict = Depends(get_current_user)):
    blogs = await blogCollection.find({}).to_list(100)
    per_page = 10
    all_blogs = []
    for x in blogs:
        all_blogs.append({
            "_id" : str(x['_id']),
            "title" : x["title"],
            "content" : x["content"],
            "author" : str(x["author"]),
            "tags" : x["tags"]
        })
   # print(all_blogs)
    total_blogs = len(all_blogs)
    total_pages = (total_blogs + per_page - 1) // per_page


    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_blogs = all_blogs[start_idx:end_idx]
    data = {
        "paginated_blogs" : paginated_blogs,
        "total_pages" : total_pages
    }
   
    return ResponseModel(data, "Blog Fetched Successfully.")

@router.get('/search/{id}', response_description="Blog fetched")
async def getSingleBlog(id: str, user: dict = Depends(get_current_user)):
    try:
        blog = await blogCollection.find_one({"_id" : ObjectId(id)})
        data = {}
        for key,value in blog.items():
                data[key] = str(value)
        print(data)
    except Exception as e:
        return ErrorResponseModel("Internal serve error",500,"Something went wrong while fetching the blog")
    return ResponseModel(data, "blog fetched successfully")

@router.delete('/{id}',response_description="Blog deleted")
async def deleteBlog(id : str , user : dict = Depends(get_current_user)):
    try: 
        blog = await blogCollection.find_one({"_id" : ObjectId(id)})
        if str(blog["author"]) != str(user["_id"]):
          return  ErrorResponseModel("Internal Server Error",500, "Invalid Author")
        await blogCollection.delete_one({"_id" : ObjectId(id)})
    except Exception as e:
        return ErrorResponseModel("Internal Server Error",500,"Something Went Wrong")
    
    return ResponseModel({},"Blog Deleted Succesfully")

@router.patch('/update-blog/{id}',response_description='Blog updated')
async def registerUser( id: str, newBlogData:UpdateBlog= Body(...), user: dict =   Depends(get_current_user)):
    try:
        newBlogData = jsonable_encoder(newBlogData)
        updateData = {}
        for key, value in newBlogData.items():
            if newBlogData[key] != None:
                updateData[key] = value
    
        await blogCollection.update_one({"_id" : ObjectId(id)}, {"$set": updateData})
    except Exception as e:
        print(e)
        return ErrorResponseModel("Internal Server Error",500,"Something Went Wrong")
    return ResponseModel({},"Blog Updated Succesfully")