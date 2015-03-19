from django.contrib.auth import login


def login_model_user(request, user):
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return user
