# Generated by Django 4.2.10 on 2024-02-29 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OSU_CSE_GMS', '0006_alter_student_graded_last_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='instructor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='OSU_CSE_GMS.instructor'),
        ),
    ]
