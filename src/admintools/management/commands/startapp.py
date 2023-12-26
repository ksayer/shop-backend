import os
from pathlib import Path

from django.conf import settings
from django.core.management.commands.startapp import Command as StartAppCommand

MANAGERS_CODE = "from django.db.models import QuerySet, Manager\n"
MODELS_CODE = """from django.db import models
from admintools.models import CoreModel

"""


class Command(StartAppCommand):
    def handle(self, **options):
        super().handle(**options)
        self.modificate_models(options.pop('name'))

    def modificate_models(self, app_name: str):
        app_path = Path()
        for _, dirs, _ in os.walk(settings.BASE_DIR):
            for dir_ in dirs:
                if dir_.endswith(app_name):
                    app_path = Path(dir_)
                    break
            if app_path:
                break
        assert app_path != ''
        app_path = settings.BASE_DIR.joinpath(app_path)
        models_dir = app_path.joinpath('models')
        os.mkdir(models_dir)
        with open(models_dir.joinpath('__init__.py'), 'w') as f:
            f.write('from .models import *')
        with open(models_dir.joinpath('managers.py'), 'w') as f:
            f.write(MANAGERS_CODE)
        with open(models_dir.joinpath('models.py'), 'w') as f:
            f.write(MODELS_CODE)
        trash_files = ['models', 'tests', 'views']

        for file_name in trash_files:
            os.remove(f'{app_path}/{file_name}.py')
