import json
from pymongo import MongoClient
from ..util.mongo_helpers import get_mongo_conn

def get_quota_info(user_id):
    db = get_mongo_conn()
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

    return user_quota_info, 200