import uuid
import datetime
import json
from ..util.cassandra_helpers import get_cassandra_conn

def get_all_datasets():
    session = get_cassandra_conn()
    stmt = """
        SELECT * FROM system_schema.tables WHERE keyspace_name = 'public';
    """
    res = session.execute(stmt)
    dataset_names = [row.table_name for row in res]

    response_object = {
        'dataset_names': dataset_names
    }
    return response_object, 200


def get_dataset_schema(dataset_name):
    session = get_cassandra_conn()
    stmt = """select column_name,type from system_schema.columns 
            where keyspace_name ='public' AND table_name='{tablename}' ;""".format(tablename=dataset_name)
    print(stmt)
    res = session.execute(stmt)
    print(res)
    types = dict()
    for r in res:
        print(r)
        types[r.column_name] = r.type

    dataset_schema = json.dumps(types) 

    response_object = {
            'dataset_schema' : dataset_schema
        }
    return response_object, 200
