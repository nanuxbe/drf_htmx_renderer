from django.conf import settings
from django.db import models
from django.utils import timezone


FEELINGS_CHOICES = [
    ('ha', 'Happy'),
    ('jo', 'Joyful'),
    ('co', 'Content'),
    ('re', 'Relaxed'),
    ('lo', 'Loved'),
    ('va', 'Valued'),
]

CARING_CHOICES = [
    ('wa', 'Walking'),
    ('me', 'Meditate'),
    ('ba', 'Bath'),
    ('co', 'Cook'),
    ('ex', 'Exercise'),
]


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Project(models.Model):

    STATES = (
        ('draft', 'draft'),
        ('running', 'running'),
        ('finished', 'finished'),
        ('cancelled', 'cancelled'),
        ('archived', 'archived'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    state = models.CharField(max_length=30, choices=STATES, default='draft', editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return self.name


class Todo(models.Model):
    description = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.description


class Feeling(models.Model):
    feels = models.CharField(max_length=2, choices=FEELINGS_CHOICES, default=None)

    def __str__(self):
        return self.feels


class Caring(models.Model):
    cares = models.CharField(max_length=2, choices=CARING_CHOICES, default=None)

    def __str__(self):
        return self.cares


class MoodTracker(models.Model):
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    emote = models.FileField(upload_to=None)
    feeling = models.ForeignKey(Feeling, blank=True, null=True, on_delete=models.CASCADE, default='ha')
    care = models.ForeignKey(Caring, blank=True, null=True, on_delete=models.CASCADE, default='co')
