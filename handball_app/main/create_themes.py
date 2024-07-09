from main.models import Theme, THEME_CHOICES

for theme_name, display_name in THEME_CHOICES:
    Theme.objects.get_or_create(name=theme_name)