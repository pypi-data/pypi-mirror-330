from django.apps import apps
from .models import SimpleTask


def get_simpletask_models():
    models = []
    for model in apps.get_models():
        if issubclass(model, SimpleTask):
            models.append(model)
    return models
