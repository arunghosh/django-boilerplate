from django.utils import timezone
from django.db import models
from django.db import transaction

from model_utils.fields import StatusField
from model_utils import Choices

from apps.account.models import User


GENDER_OPTS = (
  (0, "--"),
  (1, "Male"),
  (2, "Female"),
  (3, "Other"),
)


class Profile1(models.Model):
    field_name_2 = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True


class Profile2(models.Model):
    field_name_1 = models.CharField(max_length=10, null=True, blank=True)
    
    class Meta:
        abstract = True


class BaseProfile(models.Model):
    USER_TYPES = Choices('profile1', 'profile2', 'staff')

    user = models.OneToOneField(User, related_name="profile", primary_key=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    email = models.CharField(max_length=128)
    mobile = models.CharField(max_length=64, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_OPTS, default=0, verbose_name="Gender")
    dob = models.DateField(null=True, blank=True)
    
    user_type = StatusField(choices_name='USER_TYPES', default=USER_TYPES.staff)

    created = models.DateTimeField(default=timezone.now, verbose_name="Joined On")
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        if self.first_name:
            return self.first_name + " " + self.last_name
        return self.email

    @transaction.atomic
    def save(self, *args, **kwargs):
        self._create_user()
        super(Profile, self).save(*args, **kwargs)
        self._update_user()

    # TODO replace with signals
    def _update_user(self):
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
        self.user.save()

    def _create_user(self, *args, **kwargs):
        if not self.user:
            self.user = User.objects.create_user(
                email=self.email, 
                password='abcd1234')


class Profile(Profile1, Profile2, BaseProfile):
    pass
