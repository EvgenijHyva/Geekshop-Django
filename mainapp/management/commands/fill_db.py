from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError

from mainapp import models
import json
import os
from pathlib import Path

class Command(BaseCommand):
    source = "fixtures"
    folder = None

    def find_fixtures_folder(self, location):
        if self.source not in os.listdir(location):
            if location == settings.BASE_DIR:
                print(f"Folder <{self.source}> not found.\nCreated <{self.source}> in root.")
                os.mkdir(location / self.source)
                self.folder = location / self.source
                return
            self.find_fixtures_folder(location.parent)
        else:
            self.folder = location / self.source
            return

    def get_fixtures_files(self):
        location = Path(__file__).parent
        self.find_fixtures_folder(location)
        return os.listdir(self.folder)

    def load_from_json(self, file_name):
        with open(os.path.join(file_name), "r", encoding='utf-8') as file:
            return json.load(file)

    def find_model(self, name):
        model = models.__dict__.get(name)
        return model

    def write_data(self, model, data):
        model_batch = []
        try:
            for item in data:
                item["fields"].update({"pk": item.get("pk")})
                try:
                    model_batch.append(model(**item["fields"]))
                except ValueError as err:
                    import re
                    pk, _model_name = list(map(lambda x: x.replace("\"", ""), re.findall("\"\w+\"", f"{err}")))
                    dependency_model = models.__dict__.get(_model_name)
                    instance = dependency_model.objects.filter(pk=pk).first()
                    if instance:
                        item["fields"][_model_name.lower()] = instance
                        model_batch.append(model(**item["fields"]))
                    else:
                        print(f"Error: {err}")
            model.objects.bulk_create(model_batch, ignore_conflicts=True)
            print("Done")
        except IntegrityError:
            print("Already exists. Skipping")

    def handle(self, *args, **options):
        files = self.get_fixtures_files()
        for file in files:
            data = self.load_from_json(self.folder / file)
            model_name = file[:file.find(".")].title()
            model = self.find_model(model_name)
            self.write_data(model, data)

        if not files:
            print("Nothing to load")