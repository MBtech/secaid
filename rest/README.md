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


## Testing 
`python manage.py test`

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
- Add model and update app logic for topic related operations
- Add model and update app logic for job related operations
- Enable SSL/TLS for backend server
- Stream result set or dataset to user

## Notes
- Should we have security check for the tar files uploaded for jobs
- Right now SQL Lite database is being used during development
- The file storage parser is using werkzeug FileStorage which might need to be changed for production server
