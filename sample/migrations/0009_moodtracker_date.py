# Generated by Django 4.2.3 on 2023-08-14 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0008_remove_moodtracker_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodtracker',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]