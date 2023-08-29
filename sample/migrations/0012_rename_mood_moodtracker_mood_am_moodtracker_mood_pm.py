# Generated by Django 4.2.3 on 2023-08-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0011_delete_moodfeel_remove_moodtracker_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moodtracker',
            old_name='mood',
            new_name='mood_am',
        ),
        migrations.AddField(
            model_name='moodtracker',
            name='mood_pm',
            field=models.CharField(choices=[('VG', 'Very Good'), ('G', 'Good'), ('N', 'Neutral'), ('B', 'Bad'), ('VB', 'Very Bad')], default='Neutral', max_length=30),
        ),
    ]