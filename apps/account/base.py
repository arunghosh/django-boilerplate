from abc import abstractmethod

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import models, transaction
from django.contrib import admin
from django import forms

from apps.utils.models import AbstractTimestampModel
import apps.utils.validators as v
from .models import User


GENDER_OPTS = (
  (0, "--"),
  (1, "Male"),
  (2, "Female"),
)


class UserProfileManager(models.Manager):

    def register(self, email, password, first_name, last_name, mobile):
        user = User.objects.create_user(
            email= email,
            password= password,)
        profile = self.create(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            email=email,
            user=user,)
        return profile


class AbstractUserProfileModel(AbstractTimestampModel):
    user = models.OneToOneField(User, related_name="%(class)s_profile", null=True, blank=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    mobile = models.CharField(max_length=64, null=True, blank=True, validators = v.mobile.validators)
    address = models.CharField(max_length=512, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=64, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_OPTS, default=0, verbose_name="Gender")
    dob = models.DateField(null=True, blank=True)
    password = 'abcd1234'

    objects = UserProfileManager()

    def add_log(self):
        return self.user.add_log()

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(AbstractUserProfileModel, self).save(*args, **kwargs)
        self._create_user()
        self._update_user()

    def _update_user(self):
        '''
        Sync Data with user_profile and user
        '''
        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.email = self.email
        self.user.save()

    def _create_user(self, *args, **kwargs):
        '''
        When user is created via admin
        '''
        if not self.user:
            self.user = User.objects.create_user(
                email=self.email, 
                password=self.password)
            super(AbstractUserProfileModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True



class AbstractRegistrationForm(forms.Form):

    submit_button_name = 'Register'

    first_name = forms.CharField(label=_('First Name'))
    last_name = forms.CharField(label=_('Last Name'))
    email = forms.EmailField()
    email_confirm = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.custom_errors = []
        super(AbstractRegistrationForm, self).__init__(*args, **kwargs)

    @abstractmethod
    def create_object(self, **kwargs):
        ''' 
        You can overrride object creation in the firn save method
        ex: CustomUser.objects.register(**kwargs)
        '''
        # profile.register()
        pass

    def clean_email_confirm(self):
        ''' Check if email and confirm email are the same
        '''
        cleaned_data = super(AbstractRegistrationForm, self).clean() 
        email = cleaned_data.get('email')
        confirm = cleaned_data.get('email_confirm')
        if email != confirm:
            raise forms.ValidationError('Confirm email not matching.')
        return confirm
  
    @transaction.atomic
    def save(self):
        if self.is_valid():
            try:
                return self.create_object(**self.cleaned_data)
            except ValueError as e:
                self.custom_errors.append(str(e))
            except Exception as e:
                #TODO log
                print e
                self.custom_errors.append("Failed to register user.")
            return


class UserAdminBase(admin.ModelAdmin):
    list_display = ('name', 'email', 'created',)
    search_fields = ('name', 'email', )
    # list_filter = ('status', )
    exclude = ('user', )
    readonly_fields = ('created', 'modified', )
    
