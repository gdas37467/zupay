from fastapi import APIRouter
from routes.users import router as userRouter
from routes.blogs import router as blogRouter
from routes.dashboard import router as dashboardRouter
router = APIRouter()
router.include_router(userRouter,tags=['USERS'],prefix='/users')
router.include_router(blogRouter , tags =['BLOGS'],prefix='/blog')
router.include_router(dashboardRouter, tags=['DASHBOARD'],prefix='/dashboard')