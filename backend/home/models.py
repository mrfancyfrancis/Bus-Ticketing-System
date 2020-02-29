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

    def create_account(**fields):
        username = fields.get('username')
        email = fields.get('email')
        password = fields.get('password'),
        user = User.objects.create_user(username, email, password)
        user.is_staff = False
        #Question.objects.create(question_text=question_text, pub_date=time)

        account = PassengerAccount.objects.create(user, firstname=fields.get('firstname'), lastname=fields.get('lastname'),
                            age=fields.get('age'), birthday=fields.get('birthday'),
                            contact_no=fields.get('contact_no'))

        return [user,account]

from django.db import models

# Create your models here.
