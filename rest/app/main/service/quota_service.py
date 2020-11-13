import json
from pymongo import MongoClient


def get_quota_info(user_id):
    # Access quota collection
    userinfo_col = db['userinfo']
    user_quota_info = userinfo_col.find_one(
                                    {"user_id": user_id}, 
                                    {"remaining_quota": 1, "total_quota": 1}
                                    )
    print(user_id)
    print(user_quota_info)
    if user_quota_info is None:
        response_object = {
            'status': 'fail',
            'message': 'User not found',
        }
        return response_object, 409
    print(user_quota_info)
    return user_quota_info, 200


config = json.load(open("config.json"))
mongo_host_ip = config["mongo_ip"]
mongo_host_port = config["mongo_port"]
username = config["mongo_username"]
password = config["mongo_password"]
database = config["database"]
client = MongoClient(host=mongo_host_ip, port=mongo_host_port,
                    # username = username,
                    # password = password,
                    # authSource=database
                    )
db = client[database]