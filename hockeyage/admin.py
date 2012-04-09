from django.contrib import admin
from django.db.models import get_models, get_app

models = get_models(get_app('hockeyage'))
for model in models:
    admin.site.register(model)
