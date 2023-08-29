# Generated by Django 4.2.3 on 2023-08-14 10:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0009_moodtracker_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moodfeel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feel', models.CharField(max_length=255)),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]