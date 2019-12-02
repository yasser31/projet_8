import json
import requests
from django.core.management.base import BaseCommand
from products.models import Products, Preferences


class Command(BaseCommand):
    url = 'https://fr.openfoodfacts.org/category/'
    category = ['pizzas', 'snacks', 'Boissons', 'produits laitiers',
                'Confiseries chocolatées']

    def handle(self, *args, **kwargs):
        for ca in self.category:
            for p in range(1, 21):
                page = str(p)
                data = requests.get(self.url + ca + '/' +
                                    page + '.json').json()
                for product in data["products"]:
                    if "product_name" in product:
                        product_name = product["product_name"]
                    if "image_front_url" in product:
                        image = product["image_front_url"]
                    if "nutrition_grades" in product:
                        score = product["nutrition_grades"]
                    if "ingredients_text" in product:
                        ingredients = product["ingredients_text"]
                    if "image_nutrition_url" in product:
                        nutrition_url = product["image_nutrition_url"]
                    if "url" in product:
                        product_url = product["url"]
                    if "categories_hierarchy" in product:
                        categories = product["categories_hierarchy"][0]
                    try:
                        Products.objects.get(product_name=product_name)
                    except Products.DoesNotExist:
                        Products.objects.create(product_name=product_name,
                                                image=image,
                                                nutrition_grade=score,
                                                ingredients=ingredients,
                                                nutri_image=nutrition_url,
                                                product_url=product_url,
                                                categories=categories
                                                )
                    else:
                        pass
