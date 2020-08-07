from django.contrib import admin
from . import models


@admin.register(models.PassengerAccount)
class PassengerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'firstname',
        'lastname',
        'age',
        'birthday',
        'contact_no',
    ]
    search_fields = [
        'id',
        'firstname',
        'lastname',
    ]


@admin.register(models.BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
    search_fields = [
        'name',
    ]


@admin.register(models.CompanyAccount)
class CompanyAccountAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'firstname',
        'lastname',
        'contact_no',
        'company',
    ]
    search_fields = [
        'id',
        'firstname',
        'lastname',
    ]


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = [
        'schedule',
        'origin',
        'destination',
        'company',
    ]
    search_fields = [
        'destination',
        'origin',
    ]


@admin.register(models.Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'passenger',
        'schedule',
    ]


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'amount',
        'payment',
        'status',
        'reservation',
    ]
    search_fields = [
        'status',
    ]
