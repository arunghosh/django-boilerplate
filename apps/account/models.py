from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from apps.utils.urlresolvers import full_reverse_url
from apps.utils.mail import MailSender
from .utils import get_random_token
from .managers import UserManager, EmailAddressManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into admin site'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether user should be treated as active.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        self._create_confirm_email()

    def _create_confirm_email(self):
        if not len(self.emails.all()):
            email = EmailAddress.objects.create_primary(self)
            email.send_confirm()

    @property
    def is_confirmed(self):
        if not len(self.emails.all()):
            return False
        # TODO for mutiple emails => find if primary is verified
        return self.emails.all()[0].verified

    @property
    def name(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def __unicode__(self):
        return self.email

    @property
    def is_user_type(self):
        return not not getattr(self, 'user_type_profile', None)

    @property
    def type_str(self):
        if self.is_user_type:
            return "user_type"
        return "admin"


class UserLog(models.Model):
    user = models.ForeignKey(User, related_name='logs')
    time = models.DateTimeField(default=timezone.now)
    text = models.CharField(max_length=256)

    def __unicode__(self):
        return str(self.time) + " " + self.text


class EmailAddress(models.Model):
    user = models.ForeignKey(User, related_name="emails")
    email = models.EmailField(unique=True)
    verified = models.BooleanField(_("verified"), default=False)
    primary = models.BooleanField(_("primary"), default=False)

    objects = EmailAddressManager()

    def send_confirm(self):
        confirm = EmailConfirm.create(self)
        confirm.send()
        return confirm


class PasswordReset(models.Model):
    user = models.ForeignKey(User, related_name="password_resets")
    created = models.DateTimeField(default=timezone.now)
    key = models.CharField(max_length=64, unique=True)

    @classmethod
    def create_from_email(cls, email):
        user = User.objects.get_by_email(email)
        key = get_random_token()
        return cls._default_manager.create(user=user, key=key)

    def send(self):
        user = self.user
        context = {
            'user': user,
            'reset_url': full_reverse_url(
                'password_reset',
                kwargs={'id': user.id, 'key': self.key})
        }
        mail = MailSender(user)
        mail.compose('Password Rest', 'emails/password', context)
        mail.send_async()

    @property
    def is_expired(self):
        exp_time = self.created + timedelta(days=1)
        return exp_time < timezone.now()


class EmailConfirm(models.Model):
    email_address = models.ForeignKey(EmailAddress)
    created = models.DateTimeField(auto_now_add=True)
    confirmed = models.DateTimeField(null=True)
    key = models.CharField(max_length=64, unique=True)

    @classmethod
    def create(cls, email_address):
        token = get_random_token()
        return cls._default_manager.create(
            email_address=email_address,
            key=token)

    def send(self):
        user = self.email_address.user
        context = {
            'email': self.email_address.email,
            'key': self.key,
            'user': user,
            'confirm_url': full_reverse_url(
                'email_confirm',
                kwargs={'id': user.id, 'key': self.key}),
        }
        mail = MailSender(user)
        mail.compose('Confirmation of your account creation and Next steps',
                     'emails/confirm', context)
        mail.send_async()
        return

    def confirm(self):
        self.confirmed = timezone.now()
        self.save()
        self.email_address.verified = True
        self.email_address.save()
