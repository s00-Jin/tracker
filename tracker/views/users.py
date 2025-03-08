from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from ..serializers.users import RegisterCreateSerializer


User = get_user_model()


class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterCreateSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="Register",
        description="User Registration",
        request=RegisterCreateSerializer,
        responses=RegisterCreateSerializer,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Successfully Registered."}, status=status.HTTP_201_CREATED
        )
