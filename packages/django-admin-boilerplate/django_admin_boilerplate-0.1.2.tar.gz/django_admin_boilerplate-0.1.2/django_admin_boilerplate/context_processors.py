from .models import ThemeSetting

def theme_processor(request):
    if request.user.is_authenticated:
        theme = ThemeSetting.objects.filter(user=request.user).values_list("theme", flat=True).first() or "default"
    else:
        theme = "default"
    return {"user_theme": theme}
