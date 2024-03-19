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

@router.get('/{page}',response_description="Blogs Fetched sorted") 
async def getBlogs(page : int ,user: dict = Depends(get_current_user)):
    matching_blogs = await blogCollection.find({}).to_list(100)
    per_page = 10
    all_blogs = []
    for x in matching_blogs:
        all_blogs.append({
            "_id" : str(x['_id']),
            "title" : x["title"],
            "content" : x["content"],
            "author" : str(x["author"]),
            "tags" : x["tags"]
        })
   # print(all_blogs)

    sorted_blogs = sorted(all_blogs, key=lambda x: len(set(x["tags"]) & set(user["tags"])),reverse=True)


    matching_tag_blogs = [blog for blog in sorted_blogs if set(blog["tags"]) & set(user["tags"])]
    non_matching_tag_blogs = [blog for blog in sorted_blogs if not set(blog["tags"]) & set(user["tags"])]
    sorted_blogs = matching_tag_blogs + non_matching_tag_blogs

    total_blogs = len(sorted_blogs)
    total_pages = (total_blogs + per_page - 1) // per_page


    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_blogs = sorted_blogs[start_idx:end_idx]
    data = {
        "paginated_blogs" : paginated_blogs,
        "total_pages" : total_pages
    }
   
    return ResponseModel(data, "Blog Fetched Successfully.")