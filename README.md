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
## Run application from docker containers
> docker-compose -f local.yml up -d --build
## Live demo
> https://simple-cars-api.herokuapp.com/
