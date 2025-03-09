from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from .views.users import RegisterViewSet
from .views.rides import RideViewSet

router = DefaultRouter()
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"rides", RideViewSet, basename="ride")

urlpatterns = router.urls
