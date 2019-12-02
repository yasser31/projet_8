from django.contrib.auth.models import User
from django.db import models


class Products(models.Model):
    ''' defines the products table with attributes'''
    product_name = models.CharField(unique=True, max_length=250)
    image = models.ImageField(upload_to="images/")
    nutrition_grade = models.CharField(max_length=1)
    ingredients = models.TextField()
    nutri_image = models.ImageField(upload_to="images/", null=True, blank=True)
    product_url = models.TextField()
    categories = models.CharField(max_length=250, default="")
    is_product = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class Preferences(models.Model):
    ''' defines the preferences table with the attributes'''
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, related_name="preferences")

    def __str__(self):
        return self.product_name
