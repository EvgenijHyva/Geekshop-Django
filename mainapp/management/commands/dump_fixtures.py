from django.core.management.base import BaseCommand
from django.core import serializers
from django.conf import settings
from mainapp import models
import os

available_names = list(models.__dict__.keys())[10:]

class Command(BaseCommand):
    store_folder = "DB_loaded"
    help = f"Dumps data from database: available names: {','.join(available_names)}." \
           f"Usage manage.py dump_fixtures <name>." \
           f"All files will stored inside folder <{store_folder}>"

    def add_arguments(self, parser):
        parser.add_argument("model_name", nargs="+", type=str)

    def handle(self, *args, **options):
        if options["model_name"]:
            for name in options["model_name"]:
                self.dumps_to_json(name.title())

    def get_file_path(self, name, extension):
        if self.store_folder not in os.listdir(settings.BASE_DIR):
            os.mkdir(settings.BASE_DIR / self.store_folder)
        extension = extension if extension.startswith(".") else "."+extension
        return settings.BASE_DIR / self.store_folder / f"{name.lower() + extension}"

    def dumps_to_json(self, name):
        extension = "json"
        file_path = self.get_file_path(name, extension)
        model = models.__dict__.get(name)
        if model:
            serialized_model = serializers.serialize(extension, model.objects.all(), indent=4)
            with open(file_path, "w", encoding="utf-8") as new_file:
                new_file.write(serialized_model)
            print(f"Model <{name}> loaded in to: {file_path}")
        else:
            print(f"Model <{name}> doesn't exists! check module_name")