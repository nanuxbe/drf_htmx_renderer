# Generated by Django 4.2.3 on 2023-08-16 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0010_moodfeel'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Moodfeel',
        ),
        migrations.RemoveField(
            model_name='moodtracker',
            name='description',
        ),
        migrations.AddField(
            model_name='moodtracker',
            name='mood',
            field=models.CharField(choices=[('VG', 'Very Good'), ('G', 'Good'), ('N', 'Neutral'), ('B', 'Bad'), ('VB', 'Very Bad')], default='Neutral', max_length=30),
        ),
    ]
