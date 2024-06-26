# Generated by Django 4.2.9 on 2024-03-05 02:57

import sys
from django.db import migrations
from django.core.management import call_command

def initialize_db_with_data(apps, schema_editor):
    call_command("loaddata", "initial_data.json")


class Migration(migrations.Migration):

    dependencies = [
        ('OSU_CSE_GMS', '0010_alter_section_instruction_mode'),
    ]

    operations = [
        migrations.RunPython(initialize_db_with_data)
    ] if 'test' not in sys.argv[1:] else [] # Skip this migration if running test cases, will conflict with test data set up in test files
    
