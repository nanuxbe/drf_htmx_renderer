# Generated by Django 4.2.3 on 2023-09-01 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0017_remove_todo_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='moodtracker',
            name='What_didnt_work',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='moodtracker',
            name='what_worked',
            field=models.TextField(blank=True),
        ),
    ]
