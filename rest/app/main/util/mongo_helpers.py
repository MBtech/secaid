from flask import current_app
from pymongo import MongoClient

def get_mongo_conn():
    mongo_host_ip = current_app.config.get('MONGO_IP')
    mongo_host_port = current_app.config.get('MONGO_PORT')
    username = current_app.config.get('MONGO_USERNAME')
    password = current_app.config.get('MONGO_PASSWORD')
    database = current_app.config.get('MONGO_DATABASE')
    client = MongoClient(host=mongo_host_ip, port=mongo_host_port,
                        username = username,
                        password = password,
                        authSource=database
                        )
    db = client[database]