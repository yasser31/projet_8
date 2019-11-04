from django.contrib import admin
from products.models import Products, Preferences

# add products to admin page
admin.site.register(Products)

# add preferences to admin page
admin.site.register(Preferences)
