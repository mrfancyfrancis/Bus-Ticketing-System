from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


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


class Reservation(models.Model):
    passenger = models.ForeignKey(PassengerAccount, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)


class Payment(models.Model)
    amount = models.DecimalField()
    payment = models.CharField()
    status = models.CharField()
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)