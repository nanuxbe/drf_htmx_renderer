# Generated by Django 4.2.3 on 2023-09-04 08:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0022_alter_moodtracker_stress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moodtracker',
            name='stress',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
