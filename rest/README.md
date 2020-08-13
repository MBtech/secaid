# Backend REST Server
Working in progress backend REST Server for SE-CAID Platform

## Folder Structure
- `model`: contains all out database models
- `service`: contains all the business logic
- `controller`: contains all out application end points


## Installation 
`pip install -r requirements.txt`

## Setup
Initiate a migration folder using `init` command for alembic to perform the migrations
`python manage.py db init`

Create a migration script from detected changes in the model
`python manage.py db migrate --message 'initial database migration'`

Apply the migration script to the database
`python manage.py db upgrade`

Build the docker image: `docker image build -t secaid .`

Run the containers: `docker run -p 5000:5000 -d secaid`


## Testing 
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
