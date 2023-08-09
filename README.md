# assignment_loop
Assignment by Loop
The technologies used for the project are as follows:
- FastAPI:  Modern web framework for building RESTful APIs in Python
- Uvicorn: ASGI web server implementation for Python
- Swagger: API documentation tool which provides UI to test API enpoints.
- SQLmodel: Library for interacting with SQL databases from Python code, with Python objects.
- Postgres: SQL database for storing data.
- PGAdmin: Open Source management tool for Postgres

PGadmin and Postgres are deployed locally as docker containers. To do so run
```
docker compose -f containers.yaml up -d
```

Python dependencies are listed in app/requirement.txt. Dependecies can be installed by running
```
cd app
pip install -r requirements.txt
```

On start up, the application scans for data directory inside app folder. It specifically looks for "menu_hours.csv" with Restaurant timings,
"store_status.csv" with polling data and "timezones.csv" with timezones of all restuarant data. 

Once the data is added to the data folder, start the uvicorn server:
```
uvicorn main:app
```

The server runs on port 8000. API documentation can be accessed using Swagger UI running at /docs endpoint
```
localhost:8000/docs
```
