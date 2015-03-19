from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.db import models
from django.contrib import admin
import apps.utils.validators as v
from .models import User


GENDER_OPTS = (
  (0, "--"),
  (1, "Male"),
  (2, "Female"),
  (3, "Other"),
)


class UserProfileBase(models.Model):
    user = models.OneToOneField(User, related_name="%(class)s_profile", null=True, blank=True)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    mobile = models.CharField(max_length=64, null=True, blank=True, validators = v.mobile.validators)
    address = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_OPTS, default=0, verbose_name="Gender")
    dob = models.DateField(null=True, blank=True)
  
    created = models.DateTimeField(default=timezone.now, verbose_name="Joined On")
    modified = models.DateTimeField(auto_now=True)

    def add_log(self):
        return self.user.add_log()

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    @property
    def gender_str(self):
        num, text = GENDER_OPTS[self.gender]
        return text

    def save(self, *args, **kwargs):
        super(UserProfileBase, self).save(*args, **kwargs)
        self._update_user(*args, **kwargs)

    def _update_user(self, *args, **kwargs):
        if not self.user:
            self.user = User.objects.create_user(email=self.email, 
                username=self.email, 
                name=self.name, 
                password='abcd1234')
            super(UserProfileBase, self).save(*args, **kwargs)
        self.user.name = self.name
        self.user.email = self.email
        self.user.save()

    class Meta:
        abstract = True


class UserAdminBase(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'created',)
    search_fields = ('name', 'email', )
    list_filter = ('status', )
    exclude = ('available_timings', 'user')
    readonly_fields = ('created', 'modified', )
    
