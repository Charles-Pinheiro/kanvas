from django.http.response import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.utils import IntegrityError
from rest_framework.authentication import authenticate
from rest_framework.authtoken.models import Token

from users.serializers import UserSerializer
from .models import User


@api_view(['POST'])
def create_user(request):

    data = request.data
    try:
        username = request.data['username']
        password = request.data['password']
        is_superuser = request.data['is_superuser']
        is_staff = request.data['is_staff']
    except KeyError:
        return HttpResponseBadRequest()

    try:
        user = User.objects.create_user(**data)
    except IntegrityError:
        return Response({'message': 'This user already exists.'}, status=status.HTTP_409_CONFLICT)
        

    serialized = UserSerializer(user)

    return Response(serialized.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):

    try:
        username = request.data['username']
        password = request.data['password']
    except KeyError:
        return HttpResponseBadRequest()

    user = authenticate(username=username, password=password)

    if user:
        token = Token.objects.get_or_create(user=user)[0]
        return Response({'token': token.key})

    return Response({'message': 'Invalid user.'}, status=status.HTTP_401_UNAUTHORIZED)