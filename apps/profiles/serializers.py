from rest_framework import serializers

from apps.account.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = Profile
        fields = [f.name for f in Profile._meta.fields] + ['password']
        write_only_fields = ('password',)
        read_only_fielda = ('modified',)

    def create(self, request):
        user = User.objects.create_user(
            email=request['email'],
            password=request['password']
        )
        return Profile.objects.create(
            user=user,
            email=request['email'],
            user_type=request['user_type']
        )
