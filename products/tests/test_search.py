import requests
import unittest
from unittest.mock import Mock, patch


class TestApi(unittest.TestCase):

    @patch('products.views.requests.get')
    def test_api(self, mock_get):
        ''' mocks the api by using a patch to change the returned
            response of get function and replace it with this
            method so we can verify that the conexion to an api
            behaves correclty
            '''
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
