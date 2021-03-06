# Backend REST Server
Working in progress backend REST Server for SE-CAID Platform

## Folder Structure
- `model`: contains all out database models
- `service`: contains all the business logic
- `controller`: contains all out application end points


## Installation 
`pip install -r requirements.txt`

## Setup
Build and push the docker image: `cd rest; ./build_and_push.sh`

Make sure you have `Direct Access Grants Enabled` in the settings of the keycloak Client ID that you are using

Set appropriate settings based on the template in `app/main/util/settings.py`

Set `export SETTINGS=<path to the settings file>` to point to the settings file 

Setup port forwarding 
```
secaid port-forward -n mongodb svc/mongodb 27017:27017 &
secaid port-forward -n cassandra svc/cassandra 9042:9042 &

```

## Testing 
**Note:** Testing code is not up to date
`python manage.py test`

## Start server
`python manage.py run`

## Resources to expose
- Account login
- Account creation
- List topics
- Topic Creation
- List datasets
- Submit jobs
- Retreive results
- Get Quota Information

## TODO:
- Enable SSL/TLS for backend server
- Stream result set or dataset to user
- Celery workers to off-load job execution

## Common Problems
- Make sure that the flask app is bound to `0.0.0.0` instead of `127.0.0.1` in the docker container ([ref](https://stackoverflow.com/questions/39525820/docker-port-forwarding-not-working))

## Notes
- Should we have security check for the tar files uploaded for jobs
- Right now SQL Lite database is being used during development
- The file storage parser is using werkzeug FileStorage which might need to be changed for production server


## Reference material
- [keycloak flask example repo](https://github.com/dangtrinhnt/keycloak_flask)
- [Creating Admin for keycloak Realm](https://stackoverflow.com/questions/56743109/keycloak-create-admin-user-in-a-realm)
