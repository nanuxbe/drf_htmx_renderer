from django.conf import settings
from django.db import models


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
