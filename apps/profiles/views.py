from rest_framework.permissions import IsAuthenticated

# from apps.account.base import ProfileViewSetBase  
from apps.utils.views import AbstractFormView

from .forms import RegistrationForm
from .serializers import ProfileSerializer
from .models import Profile

# class ProfileViewSet(ProfileViewSetBase):
#     serializer_class = ProfileSerializer
#     queryset = Profile.objects.all()
#     # permission_classes = (IsAuthenticated,)


class RegisterView(AbstractFormView):
    template_name = 'form_edit.html'
    form_class = RegistrationForm
    success_message = 'Thanks for resgistering with us. Complete the regisration process by responding to the verfication email.'



