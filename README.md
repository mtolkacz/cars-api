# Simple Car API
* Django application to query vehicle data
* Download car and its make data from https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{make_name}?format=json and upload to local PostgreSQL database
* Car model rating
## Examples
### List of all cars
> GET /cars/<br>
### List of top 10 popular products
* Products selected by rating counter
> GET /popular/<br>
### Populate DB
* Add "model" and "make" keys to request body, like model - "500" and make "Fiat"<br>
> POST /cars/<br>
### Rate car model
* Need user authentication
> POST /rate/
## Technologies
* Python 3.9<br>
* Django 3.1.3<br>
* Django Rest Framework 3.12.2<br>
* PostgreSQL 13.0<br>
* Docker 19.03.8<br>
* docker-compose 1.27.4<br>
## Example env file
* Create .env file in docker-compose root directory /env/dev/.env or /env/prod/.env 
> SECRET_KEY={your_secret_key}
<br>DEBUG=1
<br>DATABASE=postgres
<br>SQL_ENGINE=django.db.backends.postgresql
<br>SQL_DATABASE=cars
<br>SQL_USER={your_username}
<br>SQL_PASSWORD={your_password}
<br>SQL_HOST=db
<br>SQL_PORT=5432
<br>POSTGRES_USER={your_username}
<br>POSTGRES_PASSWORD={your_password}
<br>POSTGRES_DB=cars
## Run application from docker containers
> docker-compose -f local.yml up -d --build

## Live demo
> https://simple-cars-api.herokuapp.com/
