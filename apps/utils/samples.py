from django.db import transaction

from apps.account.models import User


@transaction.atomic
def fill():
    ''' Fill DB with sample data
    '''
    _create_superuser()


@transaction.atomic
def _create_superuser():
    ''' Create super user
    '''
    if User.objects.all():
        return
    print "creating super user..."
    user = User.objects.create_superuser(
        email='admin@app.com',
        first_name='Admin',
        last_name='Admin',
        password='abcd1234',)
    return user
