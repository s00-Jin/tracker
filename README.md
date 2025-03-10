# Project Setup

## Clone the Repository
```sh
git clone https://github.com/s00-Jin/tracker.git
cd <repo-name>
```

## Setup Environment Variables
Create a `.env` file by copying the sample environment file:
```sh
cp .env.sample .env
```

## Run the Project with Docker
Build and start the project using Docker Compose:
```sh
docker-compose up -d --build
```

## Run Database Migrations
Execute the following commands to apply database migrations:
```sh
docker-compose exec <container_id or name> python manage.py makemigrations
```
```sh
docker-compose exec <container_id or name> python manage.py migrate
```

## Collect Static Files
```sh
docker-compose exec <container_id or name> python manage.py collectstatic --noinput
```

## Add Superuser
```sh
docker-compose exec <container_id or name> python manage.py createsuperuser
```
when prompted to add role input "admin"

## Access API Documentation
Once the setup is complete, visit:
[http://localhost/api/schema/swagger-ui/](http://localhost/api/schema/swagger-ui/)

## Manual Testing of API Using Swagger
For manual testing, first secure an access token using api/token/ endpoint:

Sample Request:
![request body](documentation/image.png)

Sample Response
![sample response](documentation/image-1.png)

## Authenticating on Swagger
Click the authentication button
![Authentication button](documentation/image-2.png)

![Adding of access token](documentation/image-3.png)

Now you can used the endpoints available on the swagger. 

In testing the one that sort by distance used Postman.  A sample curl is given below, change the access_token to the access token given above:

```sh
curl --location 'http://localhost/v1/rides/?lat=37.7749&lon=-122.4194' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNjAyNTc3LCJpYXQiOjE3NDE1OTg5NzcsImp0aSI6IjVlNDZiZDAyZjU5NDRkMDY5ZjcxOGM1ZjljNTMxYTNmIiwidXNlcl9pZCI6MX0.fY8pICMK1Sv3Vnb5c5vEl-BW-bVw9XB8HOWpJqmhr6I'
```



