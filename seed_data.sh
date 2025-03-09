#!/bin/bash

echo "🚀 Starting database seeding with 1000 rides and 2000 users..."

# Run Django shell and execute the following commands
python manage.py shell <<EOF
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from tracker.models.users import CustomUser
from tracker.models.rides import Ride, RideEvent
import random

# Create Admin User (if not exists)
admin_user, created = CustomUser.objects.get_or_create(
    email="admin@example.com",
    defaults={"first_name": "Admin", "last_name": "User", "role": "admin", "phone_number": "1234567890"}
)
if created:
    print("✅ Admin user created.")
else:
    print("ℹ️ Admin user already exists.")

# Create 1000 Riders & 1000 Drivers
users = []
for i in range(1000):
    rider, _ = CustomUser.objects.get_or_create(
        email=f"rider{i}@example.com",
        defaults={"first_name": f"Rider{i}", "last_name": "Doe", "role": "rider", "phone_number": f"10000000{i}"}
    )
    driver, _ = CustomUser.objects.get_or_create(
        email=f"driver{i}@example.com",
        defaults={"first_name": f"Driver{i}", "last_name": "Smith", "role": "driver", "phone_number": f"20000000{i}"}
    )
    users.append((rider, driver))

print(f"✅ Created {len(users) * 2} users (riders & drivers).")

# Create 1000 Rides
rides = []
statuses = ["en-route", "pickup", "dropoff"]
for i, (rider, driver) in enumerate(users):
    ride = Ride(
        status=random.choice(statuses),
        id_rider=rider,
        id_driver=driver,
        pickup_latitude=random.uniform(-90, 90),
        pickup_longitude=random.uniform(-180, 180),
        dropoff_latitude=random.uniform(-90, 90),
        dropoff_longitude=random.uniform(-180, 180),
        pickup_time=make_aware(datetime.now() - timedelta(hours=random.randint(1, 72)))  # Last 3 days
    )
    rides.append(ride)

# Bulk insert rides for efficiency
Ride.objects.bulk_create(rides)
print(f"✅ Created {len(rides)} rides.")

# Create Ride Events (Random events for last 24 hours)
ride_events = []
for ride in Ride.objects.all():
    for _ in range(random.randint(1, 5)):  # 1-5 events per ride
        event = RideEvent(
            id_ride=ride,
            description=random.choice(["Ride started", "Ride completed", "Rider cancelled"]),
            created_at=make_aware(datetime.now() - timedelta(hours=random.randint(1, 24)))  # Last 24 hours
        )
        ride_events.append(event)

# Bulk insert ride events for efficiency
RideEvent.objects.bulk_create(ride_events)
print(f"✅ Created {len(ride_events)} ride events.")

print("🎉 Database seeding completed successfully!")

EOF
