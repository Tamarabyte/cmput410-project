from django.core import serializers
import os
from django.db import models, migrations

fixture_dir = os.path.abspath(os.path.dirname(__file__))
fixture_filename = 'server_data.json'

def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=False)
    for obj in objects:
        obj.save()
    fixture.close()

def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    Node = apps.get_model("Hindlebook", "Node")

class Migration(migrations.Migration):

    dependencies = [
        ('Hindlebook', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
        ]
