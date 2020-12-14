from flask import current_app
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def get_cassandra_conn():
    cassandra_host_ip = current_app.config.get('CASSANDRA_HOST')
    cassandra_host_port = current_app.config.get('CASSANDRA_PORT')
    username = current_app.config.get('CASSANDRA_USERNAME')
    password = current_app.config.get('CASSANDRA_PASSWORD')

    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster(auth_provider=auth_provider)

    session = cluster.connect()

    return session 
