from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model


class OnlyAuthorMixin(UserPassesTestMixin):
    def test_func(self):
        object = self.get_object()
        if hasattr(object, 'username'):
            return object.username == self.request.user.username
        elif hasattr(object, 'author'):
            return object.author.username == self.request.user.username


class UserMixin:
    model = get_user_model()
    slug_url_kwarg = 'username'
    slug_field = 'username'
