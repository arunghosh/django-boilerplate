from django.db import models
from apps.account.models import User
from django.db import transaction

class FbProfileManger(models.Manager):
    
    @transaction.atomic
    def get_or_register(self, response, token):
        user = self.get_or_register_user(response)
        profile = self.get_or_register_profile(user, response, token)
        return profile
    
    def get_or_register_profile(self, user, response, token):
        try:
            profile = self.get(user=user)
        except FbProfile.DoesNotExist:
            profile = self.create(
                user = user,
                username = response['username'],
                token = token)
        return profile

    def get_or_register_user(self, response):
        email = response.get('email', None)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create(
                email = email,
                name = response['name'],
                password = '')
        return user


class FbProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=64)
    token = models.CharField(max_length=256)

    objects = FbProfileManger()
