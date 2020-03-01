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
