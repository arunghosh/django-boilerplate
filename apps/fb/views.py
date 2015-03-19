from django.shortcuts import redirect
from django.core.urlresolvers import reverse
import facebook

from apps.utils.auth import login_model_user
from .models import FbProfile


def register_and_login(request, access_token):
    try:
        response = _get_profile(access_token)
        fb_profile = FbProfile.objects.get_or_register(response, access_token)
        login_model_user(request, fb_profile.user)
    except:
        return redirect(reverse("error"))
    return redirect(reverse("home"))


def _get_profile(access_token):
    graph = facebook.GraphAPI(access_token)
    profile = graph.get_object("me")
    return profile
