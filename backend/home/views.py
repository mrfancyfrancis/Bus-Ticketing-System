from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import json
from home.models import ResponseObject

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    print(username,password)
    response = None
    if username is None or password is None or username == '' or password == '':
        #return Response({'error': 'Please provide both username and password'},
        #                status=HTTP_400_BAD_REQUEST)
        #print("No username/password")
        response = ResponseObject(HTTP_400_BAD_REQUEST, { 'Message': 'Please provide both username and password' })

    else:
        user = authenticate(username=username, password=password)
        if not user:
            #print("Invalid")
            #return Response({'error': 'Invalid Credentials'},
            #                status=HTTP_404_NOT_FOUND)
            response = ResponseObject(HTTP_404_NOT_FOUND, { 'Message': 'Invalid Credentials' })
        else:
            token, _ = Token.objects.get_or_create(user=user)
            #return Response({'token': token.key},
            #                status=HTTP_200_OK)
            data ={
                "token":token.key,
                "username":username
            }
            response = ResponseObject(HTTP_200_OK, json.dumps(data))
    return Response(response.getResponse())
