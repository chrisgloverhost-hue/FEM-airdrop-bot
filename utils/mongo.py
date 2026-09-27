import pymongo
from utils.env import MONGO_IP, MONGO_PASSWORD, MONGO_PORT, MONGO_URI, MONGO_USER


if MONGO_URI:
    CONNECTION_STRING = MONGO_URI
elif MONGO_IP and MONGO_USER and MONGO_PASSWORD:
    CONNECTION_STRING = (
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_IP}:{MONGO_PORT}/?authSource=admin"
    )
else:
    raise ValueError("Set MONGO_URI or the MONGO_INITDB connection variables")


myclient = pymongo.MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=10000)
mydb = myclient["airdrop"]
users = mydb["users"]
users.create_index(
    [("ref", pymongo.TEXT)], name="search_index", default_language="english"
)
users.create_index("userId")


def getUserInfo(id):
    user = ""
    for x in users.find({"userId": id}):
        user = x
        user["refCount"] = users.count_documents({"ref": str(id)})
    return user
