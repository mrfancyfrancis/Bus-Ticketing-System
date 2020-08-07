from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
import json
import decimal

class PassengerAccount(models.Model):
    id = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=False)
    age = models.IntegerField(blank=False)
    birthday = models.DateField(blank=False)
    contact_no = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(\+639|09)\d{9}$',
                message='Enter a valid Phone Number',
            ),
        ],
        max_length=13,
        blank=False,
        null=False,
    )
    lastname = models.CharField(max_length=50, blank=True)


class BusCompany(models.Model):
    name = models.CharField(max_length=50, blank=False)


class CompanyAccount(models.Model):
    id = models.OneToOneField('auth.User', on_delete=models.CASCADE, primary_key=True)
    firstname = models.CharField(max_length=50, blank=False)
    lastname = models.CharField(max_length=50, blank=False)
    contact_no = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^(\+639|09)\d{9}$',
                message='Enter a valid Phone Number',
            ),
        ],
        max_length=13,
        blank=False,
        null=False,
    )
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)


class Schedule(models.Model):
    schedule = models.DateTimeField()
    origin = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE)
    ticket_price = models.DecimalField(decimal_places=2, max_digits=6)
    service_fee = decimal.Decimal(50.00)

    @property
    def full_price(self):
        return str(self.ticket_price + self.service_fee)


class Reservation(models.Model):
    passenger = models.ForeignKey(PassengerAccount, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)


class Payment(models.Model):
    amount = models.DecimalField(decimal_places=2, max_digits=6)
    payment = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    checkout_id = models.CharField(max_length=50)


class ResponseObject:
    status = ''
    data = dict()
    def __init__(self, status, data):
        self.status = status
        self.data = data
    def getResponse(self):
        return json.dumps(self.__dict__)
