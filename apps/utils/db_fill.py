from django.db import transaction

from apps.account.models import AuthUser


@transaction.atomic
def fill():
    _create_superuser()


@transaction.atomic
def _create_superuser():
    if AuthUser.objects.all():
        return
    print "creating super user..."
    user = AuthUser.objects.create_superuser(
        username='admin',
        email='admin@app.com',
        name='Admin',
        password='abcd1234',)
    return user
