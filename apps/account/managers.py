from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        self._check_unique_email(email)

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(
          email,
          password=password,
          first_name=first_name,
          last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_email(self, email):
        return self.get_queryset().get(email=email)

    def _check_unique_email(self, email):
        try:
          self.get_queryset().get(email=email)
          raise ValueError("This email is already registered")
        except self.model.DoesNotExist:
          return True


class EmailAddressManager(models.Manager):

    def send_confirm(self, email):
        try:
            email_address = self.get_queryset().get(email=email)
            return email_address.send_confirm()
        except self.model.DoesNotExist:
            return None

    def create_primary(self, user):
        return self.create(
            user = user,
            email = user.email,
            primary = True)



