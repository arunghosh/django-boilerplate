from django.test import TestCase

from model_mommy import mommy

from apps.account.models import User, UserLog, EmailAddress, PasswordReset


class UserTestCase(TestCase):

    """
    Testing user object creation.
    """

    def setUp(self):
        """
        'model_mommy' tool will make the user object
        """
        self.user = mommy.make(User)

    def test_user(self):
        """
        Test whether the object is created or not. 
        """
        self.assertTrue(isinstance(self.user, User))


class UserLogTestCase(TestCase):

    """
    Testing user logs
    """

    def setUp(self):
        """
        'model_mommy' tool will make the user object
        """
        self.user_log = mommy.make(UserLog)

    def test_user_log(self):
        """
        Test whether the object is created or not. 
        """
        self.assertTrue(isinstance(self.user_log, UserLog))


class EmailAddressTestCase(TestCase):

    """
    Testing email address
    """

    def setUp(self):
        """
        'model_mommy' tool will make the user object
        """
        self.email_address = mommy.make(EmailAddress)

    def test_email_address(self):
        """
        Test whether the object is created or not. 
        """
        self.assertTrue(isinstance(self.email_address, EmailAddress))


class PasswordResetTestCase(TestCase):

    """
    Testing email address
    """

    def setUp(self):
        """
        'model_mommy' tool will make the object
        """
        self.reset_password = mommy.make(PasswordReset)

    def test_password_reset(self):
        """
        Test whether the object is created or not. 
        """
        self.assertTrue(isinstance(self.reset_password, PasswordReset))
