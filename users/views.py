from rest_framework import status, generics
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from utilsLib.permissions import AdminPermission
from users.serializers import UserSerializer
from users.models import User


class UserCreationAPIView(generics.CreateAPIView):

    permission_classes = [AdminPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListAPIView(generics.ListAPIView):

    permission_classes = [AdminPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDetailedAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [AdminPermission]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
