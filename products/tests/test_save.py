import pdb
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from products.models import Products, Preferences
from products.views import save


class TestSave(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="yasser",
                                             password="123456")
        self.client.login(username="yasser", password="123456")
        Products.objects.create(product_name="pizza")

    def test_save(self):
        ''' tests that the subsitut is saved in preferences'''
        product = Products.objects.get(product_name='pizza')
        response = self.client.get(reverse('save', args=[product.id]))

        self.assertEqual(response.templates[0].name, 'save.html')
        self.assertEqual(response.context['name'], 'pizza')
        self.assertRaises(Preferences.DoesNotExist)
