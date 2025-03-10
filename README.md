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

## Create Sample data for testing
```sh
docker-compose exec <container_id or name> bash /app/seed_data.sh
```

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

## To run the pytest
```sh
docker-compose exec <container_id or name> pytest

```



## Bonus SQL

```sh
WITH RideDurations AS (
    SELECT
        r.id AS ride_id,
        r.id_driver AS driver_id,
        DATE_TRUNC('month', pickup_event.created_at) AS month,
        EXTRACT(EPOCH FROM (dropoff_event.created_at - pickup_event.created_at)) / 3600 AS ride_duration_hours
    FROM Ride r
    JOIN RideEvent pickup_event 
        ON r.id = pickup_event.id_ride 
        AND pickup_event.description = 'Status changed to pickup'
    JOIN RideEvent dropoff_event 
        ON r.id = dropoff_event.id_ride 
        AND dropoff_event.description = 'Status changed to dropoff'
)
SELECT 
    TO_CHAR(rd.month, 'YYYY-MM') AS month,
    CONCAT(u.first_name, ' ', u.last_name) AS driver,
    COUNT(rd.ride_id) AS count_of_trips_over_1_hr
FROM RideDurations rd
JOIN CustomUser u ON rd.driver_id = u.id
WHERE rd.ride_duration_hours > 1
GROUP BY rd.month, driver
ORDER BY rd.month, count_of_trips_over_1_hr DESC;


```
