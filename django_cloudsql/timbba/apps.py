# from django.apps import AppConfig


# class ClientConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "timbba"
from django.apps import AppConfig
import os

class TimbbaConfig(AppConfig):
    name = 'timbba'
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'timbba')

