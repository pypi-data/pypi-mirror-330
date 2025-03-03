# middleware.py
from django.utils.deprecation import MiddlewareMixin
from .models import ThemeSetting

class ThemeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                request.theme = ThemeSetting.objects.get(user=request.user).theme
            except ThemeSetting.DoesNotExist:
                request.theme = "default"
        else:
            request.theme = "default"
