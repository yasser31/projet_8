from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ..models import Products, Preferences


class CreateTest(TestCase):
    def setUp(self):
        self.preference = Preferences.objects.create(product_name='pizza')
        self.product = Products.objects.create(product_name='pizza')

    def test_create(self):
        product = Products.objects.get(product_name=self.product)
        preference = Preferences.objects.get(product_name=self.preference)
        self.assertEqual(product.product_name, 'pizza')
        self.assertEqual(preference.product_name, 'pizza')

    def test_update(self):
        product = Products.objects.get(product_name="pizza")
        product.product_name = "pizza quatre fromages"
        self.assertEqual(product.product_name, "pizza quatre fromages")

    def test_delete(self):
        product = Products.objects.get(product_name="pizza")
        product.delete()
        product = Products.objects.filter(product_name="pizza").count()
        self.assertEqual(product, 0)
