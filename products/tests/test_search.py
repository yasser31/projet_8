import requests
import unittest
from unittest.mock import Mock, patch


class TestApi(unittest.TestCase):

    @patch('products.views.requests.get')
    def test_api(self, mock_get):
        url = 'https://fr.openfoodfacts.org/category/'
        products = [
            {
                "product_name": "pizza",
                "nutrition_grade": "b"
            },
        ]
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = products
        response = requests.get(url)
        self.assertEqual(response.json(), products)
