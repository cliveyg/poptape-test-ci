# poptape-address
Address microservice written in Python Flask

This microservice validates and stores address data in a Postgres database.

Please see [this gist](https://gist.github.com/cliveyg/cf77c295e18156ba74cda46949231d69) to see how this microserv
cie works as part of the auction system software.

### API routes

```
/address [GET] (Authenticated)

Returns a list of addresses for the authenticated user. 
Possible return codes: [200, 404, 401, 502]

/address [POST] (Authenticated)

Returns a UUID of the address if create is successful. 
Possible return codes: [200 400 401 422]

/address/<uuid> [DELETE] (Authenticated)

Deletes the address resource defined by the UUID in the URL. 
Possible return codes: [204, 401]

/address/<uuid> [GET] (Authenticated)

Returns the address resource defined by the UUID in the URL. 
Possible return codes: [200, 401, 404]

/address/status [GET] (Unauthenticated)

Returns a JSON message indicating system is running 
Possible return codes: [200]

/address/countries [GET] (Unauthenticated)

Returns the list of ISO-3166 countries. 
Fields are 'name' and 'iso_code'. Possible return codes: [200, 401, 404, 502]

/address/admin/address [GET] (Authenticated)

Returns a paginated list of all addresses. Possible return codes: [200, 401, 404, 500] 
```

#### Notes:
Editing of an already existing address is not allowed at present. This is a business rule rather than for any technical reason. Microservice uses JWT and relies on an external service to authenticate and authorize. This normally sits on the same internal docker network when this service is dockerized. 

To run this microservice it is recommended to use a Python virtual environment and run `pip install -r requirements.txt`. 

Address schema for UK has been added. Validates UK postcode based official UK Gov regex. Also checks that at least one of house\_name or house\_number is present.

Two scripts have been added to load country data into the live or test dbs. The scripts are `load_countries_into_live.py` and `load_countries_into_test.py`. Both utilise the pytest framework to load data. They can be run using the commands `pytest app/tests/load_countries_into_live.py` or `pytest app/tests/load_countries_into_test.py`

#### Rate limiting:
In addition most routes will return an HTTP status of 429 if too many requests are made in a certain space of time. The time frame is set on a route by route basis.

#### Tests:
Tests can be run from app root using: `pytest --cov=app app/tests`

#### Address fields allowed in post:
* house\_name
* house\_number
* address\_line\_1
* address\_line\_2
* address\_line\_3
* state\_region\_county
* post\_zip\_code
* iso\_code - Three digit ISO-3166 code - checked by JSON schema.

All fields apart from iso\_code are optional but will be eventually validated in more detail by JSON schemas for each individual country. 

#### Docker:
This app can now be run in Docker using the included docker-compose.yml and Dockerfile. The database and roles still need to be created manually after successful deployment of the app in Docker. It's on the TODO list to automate these parts :-)

#### TODO:
* Add more admin only routes for bulk actions etc.
* Dockerize the application and run under wsgi.
* Need to add per country json schemas - added UK specific only at present.
* Possibly add address lookup on per country basis - i.e. for UK use https://api.getAddress.io
* Only 95% test coverage - Most of the missing parts are due to mocking of authenticating decorator.
* Make code pep8 compliant even though imo pep8 code is uglier and harder to read ;-)
* Automate docker database creation and population.
