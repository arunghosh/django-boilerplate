from django.test import TestCase
from apps.account.models import AuthUser as User
from .models import FbProfile


class FbTest(TestCase):

  def setUp(self):
    User.objects.create_user(
        email="arun@g.com", 
        password="abncd",
        name="Arun G")

  def _get_response(self, email, name, username):
    return {
      'email': email,
      'name': name, 
      'username': username,
    }

  def test_register_new_user(self):
    response = self._get_response('arunghosh@gmail.com', 'Arun Ghosh', 'arunghosh')
    profile = FbProfile.objects.get_or_register(response, '3859ankasdkokf')
    self.assertEqual(profile.username, response['username'])
    self.assertEqual(profile.user.email, response['email'])

  def test_register_old_user(self):
    response = self._get_response('arun@g.com', 'Arun G', 'arung')
    profile = FbProfile.objects.get_or_register(response, '3859ankasdkokf')
    self.assertEqual(profile.username, response['username'])
    self.assertEqual(profile.user.email, response['email'])
