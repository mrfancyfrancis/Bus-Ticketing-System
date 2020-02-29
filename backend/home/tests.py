from unittest.mock import patch
from django.test import TestCase

from home.models import PassengerAccount


def sample_passenger_user(**kwargs):
    return PassengerAccount.create_account(username='memeuser', email='meme@meme.com', password='password', firstname='mememan', lastname='mauricio',
                                                age=69, birthday='1969-04-20', contact_no="09175982186")


class AccountTests(TestCase):
    def test_passenger_account(self):
        acc = sample_passenger_user()
        print(acc)
        self.assertEqual(acc.firstname, 'mememan')
