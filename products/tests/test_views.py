import unittest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from products.models import Products, Preferences


class TestViews(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_index(self):
        ''' tests get request to the index page'''
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "index.html")

    def test_contact(self):
        ''' tests the get request to contact page'''
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "contact.html")

    def test_legal_notice(self):
        ''' tests get request to legal notice'''
        response = self.client.get("/legal/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, "notice.html")

    def test_login_required(self):
        ''' tests that the login required is functionnal when needed'''
        response = self.client.get("/preferences/", follow=True)
        self.assertEqual(
            response.redirect_chain[0][0],
            '/accounts/login/?next=/preferences/'
        )

    def test_search(self):
        ''' tests the product search'''
        response = self.client.get("/search/", data={"query": "coca"})
        self.assertEqual(response.templates[0].name, "result.html")
        self.assertRaises(IndexError)
        self.assertTrue(response.context)
