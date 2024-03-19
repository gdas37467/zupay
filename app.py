import uvicorn
from fastapi import FastAPI
from routes.main import router as mainRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#cors setting
origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(JWTTokenVerificationMiddleware, include_paths = ("api/v1/users/update-profile"))


# @app.get("/", tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app!"}


app.include_router(mainRouter,prefix='/api/v1')

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

