from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
import json
from home.models import ResponseObject, PassengerAccount
import home.utils

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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book(request):
    user = PassengerAccount.objects.filter(id=request.user).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, {'Message': 'Invalid User'}).getResponse())

    

    payload = {
                "totalAmount": {
                    "value": 100,
                    "currency": "PHP",
                    "details": {
                        "discount": 0,
                        "serviceCharge": 0,
                        "shippingFee": 0,
                        "tax": 0,
                        "subtotal": 100
                    }
                },
                "buyer": {
                    "firstName": user.firstname,
                    "middleName": "",
                    "lastName": user.firstname,
                    "birthday": user.birthday.strftime('%Y-%m-%d'),
                    "customerSince": "1995-10-24",
                    "sex": "M",
                    "contact": {
                        "phone": user.contact_no,
                        "email": request.user.username
                    },
                    "shippingAddress": {
                        "firstName": "",
                        "middleName": "",
                        "lastName": "",
                        "phone": "",
                        "email": "",
                        "line1": "",
                        "line2": "",
                        "city": "",
                        "state": "",
                        "zipCode": "",
                        "countryCode": "",
                        "shippingType": ""
                    },
                    "billingAddress": {
                        "line1": "",
                        "line2": "",
                        "city": "",
                        "state": "",
                        "zipCode": "",
                        "countryCode": "PH"
                    }
                },
                "items": [
                    {
                        "name": "Canvas Slip Ons",
                        "quantity": 1,
                        "code": "CVG-096732",
                        "description": "Shoes",
                        "amount": {
                            "value": 100,
                            "details": {
                                "discount": 0,
                                "serviceCharge": 0,
                                "shippingFee": 0,
                                "tax": 0,
                                "subtotal": 100
                            }
                        },
                        "totalAmount": {
                            "value": 100,
                            "details": {
                                "discount": 0,
                                "serviceCharge": 0,
                                "shippingFee": 0,
                                "tax": 0,
                                "subtotal": 100
                            }
                        }
                    }
                ],
                "redirectUrl": {
                    "success": "https://www.merchantsite.com/success",
                    "failure": "https://www.merchantsite.com/failure",
                    "cancel": "https://www.merchantsite.com/cancel"
                },
                "requestReferenceNumber": "1551191039",
                "metadata": {}
            }

    return Response(content)
