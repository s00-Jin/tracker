from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter
from .views.users import RegisterViewSet

router = DefaultRouter()
router.register(r"register", RegisterViewSet, basename="register")

urlpatterns = router.urls
