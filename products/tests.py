from django.test import TestCase


class ProductsTestCase(TestCase):

    def test_index(self):
        """
        Test index view
        """
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
