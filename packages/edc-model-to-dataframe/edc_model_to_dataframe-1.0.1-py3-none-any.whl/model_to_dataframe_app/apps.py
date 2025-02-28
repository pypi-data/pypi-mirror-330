from django.apps import AppConfig as DjangoApponfig
from django.core.management import color_style

style = color_style()


class AppConfig(DjangoApponfig):
    name = "model_to_dataframe_app"
    default_auto_field = "django.db.models.BigAutoField"
