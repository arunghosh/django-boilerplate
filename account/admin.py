from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):

    def save_model(self, request, user, form, change):
        if user.password:
            user.set_password(user.password)
        user.save()

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
