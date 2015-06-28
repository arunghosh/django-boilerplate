from django.contrib import admin
from .models import Profile, Profile1, Profile2, BaseProfile


BASE_FIELDS = [f.name for f in BaseProfile._meta.fields]
BASE_FIELDS.remove('modified')


class Profile1Proxy(Profile):
    class Meta:
        verbose_name = 'Profile1'
        proxy = True


class Profile2Proxy(Profile):
    class Meta:
        verbose_name = 'Profile2'
        proxy = True


@admin.register(Profile1Proxy)
class ClientAdmin(admin.ModelAdmin):
    fields = BASE_FIELDS + [f.name for f in Profile1._meta.fields]

    def get_queryset(self, request):
        return super(ClientAdmin, self).get_queryset(request).filter(user_type='profile1')


@admin.register(Profile2Proxy)
class TrainerAdmin(admin.ModelAdmin):
    fields = BASE_FIELDS + [f.name for f in Profile2._meta.fields]

    def get_queryset(self, request):
        return super(TrainerAdmin, self).get_queryset(request).filter(user_type='profile2')
