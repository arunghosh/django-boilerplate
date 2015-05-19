from django.test import TestCase
from apps.account.models import User, PasswordReset

from model_mommy import mommy

from apps.account.forms import RegistrationForm, PasswordResetForm, LoginForm


class RegistrationFormTest(TestCase):

    """
    Test case for user registration
    """

    def setUp(self):
        """
        Setting up initial data
        """
        self.data = {
            'first_name': 'test',
            'last_name':  'user',
            'email': 'test@test1.com',
            'email_confirm': 'test@test1.com',
            'password': 'Abcd@1234'
        }

    def test_0_valid_form(self):
        """
        Testing valid registration
        """
        form = RegistrationForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_1_invalid_form(self):
        """
        Testing invalid registration
        """
        self.data['password'] = 'abc'
        form = RegistrationForm(data=self.data)
        self.assertFalse(form.is_valid())


class PasswordResetFormTest(TestCase):

    """
    Test case for resetting the password 
    """

    def setUp(self):
        """
        creating model instance using model mommy and initiaizing data
        """
        self.reset_password = mommy.make(PasswordReset)
        self.data = {
            'submit_button_name': 'Reset Password',
            'password': 'Bcda@1234',
            'confirm_password': 'Bcda@1234',
            'key': self.reset_password.key
        }

    def test_0_valid_form(self):
        """
        Testing with clean form data
        """
        form = PasswordResetForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_1_invalid_form(self):
        """
        Testing with wrong password match
        """
        self.data['confirm_password'] = 'bcda1244'
        form = PasswordResetForm(data=self.data)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):

    """
    Test case for user login
    """

    def setUp(self):
        """
        creating model instance using model mommy and initiaizing data
        """
        # self.user = mommy.make(User)
        self.data = {
            'submit_button_name': 'Login',
            'email': 'test@test1.com',
            'password': 'Abcd@1234'
        }

    def test_0_valid_login(self):
        """
        Testing user login with clean form data
        """
        form = LoginForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_1_invalid_login(self):
        """
        Testing user login with wrong user name and/or password
        """
        self.data['email'] = ''
        form = LoginForm(data=self.data)
        #test fails. need to check one more time.
        self.assertFalse(form.is_valid())
