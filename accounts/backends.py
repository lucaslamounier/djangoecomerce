# coding=utf-8
from .models import User
from django.contrib.auth.backends import ModelBackend as BaseModelBackend

class ModelBackend(BaseModelBackend):

    def authenticate(self, username=None, password=None):
        if not username is None:
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                pass
