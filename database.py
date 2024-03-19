import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()



MONGO_URL = os.getenv('MONGOURL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

database = client.zupay

usersCollection = database.get_collection("users")
blogCollection = database.get_collection("blogs")