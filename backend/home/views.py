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
from home.models import ResponseObject, PassengerAccount, Reservation, Payment, Schedule
from home import utils
import decimal

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
            account = PassengerAccount.objects.filter(id=user).last()
            '''
            
            account, created = PassengerAccount.objects.get_or_create(
                first_name='Firstname',
                last_name='Lastname',
                age=74,
                birthday=,
                contact_no=
            )
            '''
            data ={
                "token":token.key,
                "username":username,
                "info":{
                    'firstname': account.firstname,
                    'lastname': account.lastname,
                    'age': account.age,
                    'birthday': account.birthday.strftime('%Y-%m-%d'),
                    'contact_no': account.contact_no
                }
            }
            response = ResponseObject(HTTP_200_OK, json.dumps(data))
    return Response(response.getResponse())

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book(request):
    '''

    :param request:
    schedule: schedule to book

    :return:
    '''
    user = PassengerAccount.objects.filter(id=request.user).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, {'Message': 'Invalid User'}).getResponse())
    schedule = Schedule.objects.filter(id=request.data.get("schedule")).last()
    reservation = Reservation(
        passenger=user,
        schedule=schedule
    )
    reservation.save()
    payment = Payment(
        amount=decimal.Decimal(schedule.full_price),
        payment="{} to {} {}".format(schedule.origin, schedule.destination, schedule.company.name),
        status='Pending',
        reservation=reservation,
        checkout_id='None',
    )
    payment.save()
    payload = {
                "totalAmount": {
                    "value": int(schedule.ticket_price) + 50,
                    "currency": "PHP",
                    "details": {
                        "discount": 0,
                        "serviceCharge": 50,
                        "shippingFee": 0,
                        "tax": 0,
                        "subtotal": int(schedule.ticket_price)
                    }
                },
                "buyer": {
                    "firstName": user.firstname,
                    "middleName": "",
                    "lastName": user.lastname,
                    "birthday": user.birthday.strftime('%Y-%m-%d'),
                    "customerSince": "",
                    "sex": "",
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
                        "name": "{} to {} {}".format(schedule.origin, schedule.destination, schedule.company.name),
                        "quantity": 1,
                        "code": (schedule.company.name[3:]+'-'+format(schedule.id,'06d')),
                        "description": "Reservation Bus Ticket",
                        "amount": {
                            "value": int(schedule.ticket_price),
                            "details": {
                                "discount": 0,
                                "serviceCharge": 50,
                                "shippingFee": 0,
                                "tax": 0,
                                "subtotal": int(schedule.ticket_price)
                            }
                        },
                        "totalAmount": {
                            "value": int(schedule.ticket_price),
                            "details": {
                                "discount": 0,
                                "serviceCharge": 50,
                                "shippingFee": 0,
                                "tax": 0,
                                "subtotal": int(schedule.ticket_price)
                            }
                        }
                    }
                ],
                "redirectUrl": {
                    "success": ("http://localhost:5000/payment/approved?id="+str(payment.id)),
                    "failure": "http://localhost:5000/payment/unsuccess/",
                    "cancel": "http://localhost:5000/payment/unsuccess/"
                },
                "requestReferenceNumber": "1551191039",
                "metadata": {}
            }
    print(payload)
    response = utils.createTransaction(payload)
    payment.checkout_id = response['checkoutId']
    payment.save()
    data = {
        "payment_url": response['redirectUrl'],
        'payment_details': {
            'amount': str(payment.amount),
            'payment': "Reservation fee from {} to {}".format(schedule.origin, schedule.destination),
            'status': 'Pending',
            'checkout_id': response['checkoutId'],
        },
    }
    response = ResponseObject(HTTP_200_OK, data)
    return Response(response.getResponse())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserInfo(request):
    print(request.user, request.user.id)
    user = PassengerAccount.objects.filter(id=request.user.id).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, { 'Message': 'Invalid Credentials' })).getResponse()
    data ={
        "email":request.user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'age': user.age,
        'birthday': user.birthday.strftime('%Y-%m-%d'),
        'contact_no': user.contact_no,
        'address': user.address
    }
    response = ResponseObject(HTTP_200_OK, json.dumps(data))
    return Response(response.getResponse())

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getReservations(request):
    print(request.user, request.user.id)
    user = PassengerAccount.objects.filter(id=request.user.id).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, { 'Message': 'Invalid Credentials' })).getResponse()
    Reservations = Reservation.objects.filter(passenger=user)
    print(Reservations)
    reservations = []
    for R in list(Reservations):
        r = {
                'id':R.id,
                'date':R.schedule.schedule.strftime('%Y-%m-%d'),
                'time':R.schedule.schedule.strftime('%I:%M %p'),
                'company':R.schedule.company.name,
                'ticket_number':'#'+format(R.id,'011d'),
                'status': Payment.objects.filter(reservation=R).last().status
        }
        reservations.append(r)
    data ={
        "user":request.user.username,
        'reservations': reservations
    }
    response = ResponseObject(HTTP_200_OK, json.dumps(data))
    return Response(response.getResponse())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getUserAvailableSchedule(request):
    print(request.user, request.user.id)
    user = PassengerAccount.objects.filter(id=request.user.id).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, { 'Message': 'Invalid Credentials' })).getResponse()
    Reservations = Reservation.objects.filter(passenger=user)
    Schedules = Schedule.objects.all()
    for R in list(Reservations):
        Schedules = Schedules.exclude(id=R.schedule.id)
    print(Schedules)
    schedules = []
    for S in list(Schedules):
        s = {
            'id': S.id,
            'date': S.schedule.strftime('%Y-%m-%d'),
            'time': S.schedule.strftime('%H:%M'),
            'origin': S.origin,
            'destination': S.destination,
            'company': S.company.name,
            'ticket_fee': str(S.ticket_price),
            'total_fee': S.full_price
        }
        schedules.append(s)
    response = ResponseObject(HTTP_200_OK, schedules)
    return Response(response.getResponse())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAllSchedules(request):
    print(request.user, request.user.id)
    user = PassengerAccount.objects.filter(id=request.user.id).last()
    if not user:
        return Response(ResponseObject(HTTP_404_NOT_FOUND, { 'Message': 'Invalid Credentials' })).getResponse()
    Schedules = Schedule.objects.all()
    print(Schedules)
    schedules = []
    for S in list(Schedules):
        s = {
                'id':S.id,
                'date':S.schedule.strftime('%Y-%m-%d'),
                'time':S.schedule.strftime('%H:%M'),
                'origin':S.origin,
                'destination':S.destination,
                'company':S.company.name,
                'ticket_fee':str(S.ticket_price),
                'total_fee':S.full_price
        }
        schedules.append(s)
    response = ResponseObject(HTTP_200_OK, schedules)
    return Response(response.getResponse())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirmPayment(request):
    payment_id = request.data.get('payment_id')
    payment = Payment.objects.filter(id=payment_id).last()
    payment.status = 'Approved'
    payment.save()
    p = {
        'payment': payment.payment,
        'amount': str(payment.amount),
        'status': payment.status,
        'checkout': payment.checkout_id
    }
    response = ResponseObject(HTTP_200_OK, p)
    return Response(response.getResponse())
