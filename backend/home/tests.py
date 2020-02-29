from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase

from home.models import PassengerAccount

'''
username='memeuser', email='meme@meme.com', password='password', firstname='mememan', lastname='mauricio',
                                                age=69, birthday='1969-04-20', contact_no="09175982186"
'''
def sample_passenger_user(username='memeuser', email='meme@meme.com', password='password', firstname='mememan', lastname='mauricio',
                                                age=69, birthday='1969-04-20', contact_no="09175982186"):
    user = User.objects.create_user(username, email, password)
    return PassengerAccount.objects.create(id=user, firstname=firstname, lastname=lastname, age=age, birthday=birthday, contact_no=contact_no)

class AccountTests(TestCase):
    def test_passenger_account(self):
        acc = sample_passenger_user()
        self.assertEqual(acc.firstname, 'mememan')
